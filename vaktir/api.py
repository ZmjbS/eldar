import logging
import django_filters
from rest_framework import routers, serializers, viewsets,filters,status
from vaktir.models import Timabil,Starfsstod,Tegund,Vakt,Felagi,Skraning,Vaktaskraning
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.db.models import Prefetch, Sum, Case, When, IntegerField
from django.db import connection

logger = logging.getLogger(__name__)


# ------ Starfsstod ---------

# Serializers define the API representation.
class StarfsstodSerializer(serializers.ModelSerializer ):
	class Meta:
		model = Starfsstod
		fields = ('__all__')

# ViewSets define the view behavior.
class StarfsstodViewSet(viewsets.ModelViewSet):
	queryset = Starfsstod.objects.all()
	serializer_class = StarfsstodSerializer


# ------ Timabil ---------

# Serializers define the API representation.
class TimabilSerializer(serializers.ModelSerializer ):
	class Meta:
		model = Timabil
		fields = ('__all__')

# ViewSets define the view behavior.
class TimabilViewSet(viewsets.ModelViewSet):
	queryset = Timabil.objects.all()
	serializer_class = TimabilSerializer


# ------ Tegund ---------

# Serializers define the API representation.
class TegundSerializer(serializers.ModelSerializer ):
	class Meta:
		model = Tegund
		fields = ('__all__')

# ViewSets define the view behavior.
class TegundViewSet(viewsets.ModelViewSet):
	queryset = Tegund.objects.all()
	serializer_class = TegundSerializer


# ------ Vakt ---------

# Serializers define the API representation.
class VaktSerializer(serializers.ModelSerializer ):
	skradir = serializers.IntegerField(read_only=True)
	_timabil = TimabilSerializer(source='timabil', required=False, many=False)
	class Meta:
		model = Vakt
		fields = ('id', 'timabil', '_timabil', 'starfsstod', 'tegund', 'lagmark', 'hamark','skradir')

# ViewSets define the view behavior.
class VaktViewSet(viewsets.ModelViewSet):
	with connection.cursor() as cursor:
		cursor.execute('SELECT distinct(id) FROM vaktir_skraning  group by felagi_id order by timastimpill desc')
		skraningIds = cursor.fetchall()


	queryset = Vakt.objects.all().select_related('timabil').annotate(skradir=Sum(
		Case(
			When(vaktaskraning__skraning__in=skraningIds, then=1),
			default=0, 
			output_field=IntegerField()
		)
	))
	serializer_class = VaktSerializer
	filter_backends =  (filters.DjangoFilterBackend,)
	filter_fields = ('starfsstod',)


# ------ Felagi ---------

# Serializers define the API representation.
class FelagiSerializer(serializers.ModelSerializer ):
	class Meta:
		model = Felagi
		fields = ('__all__')

# ViewSets define the view behavior.
class FelagiViewSet(viewsets.ModelViewSet):
	queryset = Felagi.objects.all()
	serializer_class = FelagiSerializer
	filter_backends =  (filters.DjangoFilterBackend,)
	filter_fields = ('netfang',)



# ------ Vaktaskraning ---------

# Serializers define the API representation.
class VaktaskraningSerializer(serializers.ModelSerializer ):
	class Meta:
		model = Vaktaskraning
		fields = ('__all__')

# ViewSets define the view behavior.
class VaktaskraningViewSet(viewsets.ModelViewSet):
	queryset = Vaktaskraning.objects.all()
	serializer_class = VaktaskraningSerializer
	filter_backends =  (filters.DjangoFilterBackend,)
	filter_fields = ('felagi',)




# ------ Skraning ---------

class CustomSerializer(serializers.Serializer):
	hefst = serializers.ReadOnlyField(source='vakt.timabil.hefst', read_only=True)
	lykur = serializers.ReadOnlyField(source='vakt.timabil.lykur', read_only=True)
	starfsstod = StarfsstodSerializer(source='vakt.starfsstod', read_only=True)	
	tegund = TegundSerializer(source='vakt.tegund', read_only=True)
	class Meta:
		fields = ('__all__')



# Serializers define the API representation.
class SkraningSerializer(serializers.ModelSerializer):
	vaktir = serializers.ListField(child=serializers.IntegerField(), required=False)
	_vaktir = CustomSerializer(source='vaktaskraning',required=False, many=True, read_only=True)
	class Meta:
		model = Skraning
		fields = ('id', 'athugasemd', 'felagi', 'vaktir', '_vaktir')
		

	def create(self, validated_data):
		vaktir = validated_data.pop('vaktir')
		skraning = Skraning.objects.create(**validated_data)
		toInsert = []
		for vakt in vaktir:
			toInsert.append(Vaktaskraning(
				skraning=skraning, 
				felagi=skraning.felagi,
				vakt_id=vakt
			))
			
		Vaktaskraning.objects.bulk_create(toInsert)
		return skraning



# ViewSets define the view behavior.
class SkraningViewSet(viewsets.ModelViewSet):
	queryset = Skraning.objects.all().prefetch_related(
		Prefetch('vaktaskraning', queryset=Vaktaskraning.objects.select_related())
	)
	serializer_class = SkraningSerializer
	filter_backends =  (filters.DjangoFilterBackend, )
	filter_fields = ('felagi')
	
	def create(self, request, pk=None):		

		serializer = SkraningSerializer(data=request.data)		

		if serializer.is_valid():
			serializer.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def list(self, request):
		try:
			skraningar = Skraning.objects.filter(felagi_id=request.query_params['felagi']).latest('timastimpill')
		except Skraning.DoesNotExist:
			skraningar = None
		
		serializer = SkraningSerializer(skraningar, many=False)
		return Response(serializer.data)


	


def createRouter():
	router = routers.DefaultRouter()
	router.register(r'starfsstod', StarfsstodViewSet)
	router.register(r'timabil', TimabilViewSet)	
	router.register(r'tegund', TegundViewSet)		
	router.register(r'vakt', VaktViewSet)	
	router.register(r'felagi', FelagiViewSet)
	router.register(r'skraning', SkraningViewSet)
	router.register(r'vaktaskraning', VaktaskraningViewSet)	
	
	return router




