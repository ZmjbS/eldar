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
	hefst = serializers.DateTimeField(source='timabil_hefst', required=False, read_only=True)
	lykur = serializers.DateTimeField(source='timabil_lykur', required=False, read_only=True)	
	class Meta:
		model = Vakt
		fields = ('id', 'timabil', 'hefst', 'lykur', 'hefst', 'starfsstod', 'tegund', 'lagmark', 'hamark','skradir')

# ViewSets define the view behavior.
class VaktViewSet(viewsets.ModelViewSet):
	# with connection.cursor() as cursor:
	# 	cursor.execute('SELECT distinct(id) FROM vaktir_skraning  group by felagi_id order by timastimpill desc')
	# 	skraningIds = cursor.fetchall()


	queryset = Vakt.objects.raw("""
		SELECT v.*, count(s.id) as skradir , t.hefst as timabil_hefst, t.lykur as timabil_lykur, t.id as timabil_id FROM vaktir_vakt as v
		left outer join (
			SELECT * FROM vaktir_vaktaskraning where vaktir_vaktaskraning.skraning_id in (SELECT id from ((SELECT DISTINCT ON (id), felagi_id, timastimpill
			 FROM vaktir_skraning  group by felagi_id order by timastimpill desc))
		) as s on s.vakt_id = v.id
		join vaktir_timabil as t on t.id = v.timabil_id
		GROUP BY v.id
	""")
	serializer_class = VaktSerializer


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
	queryset = Skraning.objects.raw(
		'SELECT distinct(id), vaktir_skraning.timastimpill, vaktir_skraning.felagi_id FROM vaktir_skraning  group by felagi_id order by timastimpill desc'
	)
	# 	Prefetch('vaktaskraning', queryset=Vaktaskraning.objects.all())
	# )
	serializer_class = SkraningSerializer
	
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




