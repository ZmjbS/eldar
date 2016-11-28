from rest_framework import routers, serializers, viewsets
from vaktir.models import Timabil,Starfsstod,Tegund,Vakt,Felagi,Skraning,Vaktaskraning


# ------ Starfsstod ---------

# Serializers define the API representation.
class StarfstodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Starfsstod
        fields = ('__all__')

# ViewSets define the view behavior.
class StarfstodViewSet(viewsets.ModelViewSet):
    queryset = Starfsstod.objects.all()
    serializer_class = StarfstodSerializer


# ------ Timabil ---------

# Serializers define the API representation.
class TimabilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Timabil
        fields = ('__all__')

# ViewSets define the view behavior.
class TimabilViewSet(viewsets.ModelViewSet):
    queryset = Timabil.objects.all()
    serializer_class = TimabilSerializer


# ------ Tegund ---------

# Serializers define the API representation.
class TegundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tegund
        fields = ('__all__')

# ViewSets define the view behavior.
class TegundViewSet(viewsets.ModelViewSet):
    queryset = Tegund.objects.all()
    serializer_class = TegundSerializer


# ------ Vakt ---------

# Serializers define the API representation.
class VaktSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vakt
        fields = ('__all__')

# ViewSets define the view behavior.
class VaktViewSet(viewsets.ModelViewSet):
    queryset = Vakt.objects.all()
    serializer_class = VaktSerializer


# ------ Felagi ---------

# Serializers define the API representation.
class FelagiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Felagi
        fields = ('__all__')

# ViewSets define the view behavior.
class FelagiViewSet(viewsets.ModelViewSet):
    queryset = Felagi.objects.all()
    serializer_class = FelagiSerializer


# ------ Skraning ---------

# Serializers define the API representation.
class SkraningSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skraning
        fields = ('__all__')

# ViewSets define the view behavior.
class SkraningViewSet(viewsets.ModelViewSet):
    queryset = Skraning.objects.all()
    serializer_class = SkraningSerializer




# ------ Vaktaskraning ---------

# Serializers define the API representation.
class VaktaskraningSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vaktaskraning
        fields = ('__all__')

# ViewSets define the view behavior.
class VaktaskraningViewSet(viewsets.ModelViewSet):
    queryset = Vaktaskraning.objects.all()
    serializer_class = VaktaskraningSerializer


	


def createRouter():
	router = routers.DefaultRouter()
	router.register(r'starfstod', StarfstodViewSet)
	router.register(r'timabil', TimabilViewSet)	
	router.register(r'tegund', TegundViewSet)		
	router.register(r'vakt', VaktViewSet)	
	router.register(r'felagi', FelagiViewSet)
	router.register(r'skraning', SkraningViewSet)
	router.register(r'vaktaskraning', VaktaskraningViewSet)	
		
		
	
	
	return router




