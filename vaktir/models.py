from django.db import models

class Timabil(models.Model):
	hefst = models.DateTimeField()
	lykur = models.DateTimeField()

class Stada(models.Model):
	nafn = models.CharField(max_length=32)

class Tegund(models.Model):
	nafn = models.CharField(max_length=32)

class Vakt(models.Model):
	timabil = models.ForeignKey(Timabil)
	stada = models.ForeignKey(Stada)
	lagmark = models.SmallIntegerField()
	hamark = models.SmallIntegerField()
	tegund = models.ForeignKey(Tegund)

class Felagi(models.Model):
	kennitala = models.IntegerField()
	nafn = models.CharField(max_length=32)
	simi = models.IntegerField()
	netfang = models.CharField(max_length=32)
	geta =  = models.PositiveSmallIntegerField(blank=True)

class Skraning(models.Model):
	felagi = models.ForeignKey(Felagi)
	vakt = models.ForeignKey(Vakt)
	SVORUN_VALMOGULEIKAR = (
        (0, 'Nei'),
        (1, 'Já'),
        (2, 'Kannski'),
    )
    svorun = models.PositiveSmallIntegerField(choices=SVORUN_VALMOGULEIKAR,default=0)
