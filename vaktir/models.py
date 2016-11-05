from django.db import models
from django.contrib.auth.models import User

class Timabil(models.Model):
	# Hver vakt hefur sitt tímabil. Til að einfalda uppsetningu vakta eru
	# skilgreind nokkur tímabil og svo vöktunum úthlutað þeim. Þannig er líka
	# auðveldara að hnika til vöktum; skeyta tveimur saman eða stytta vaktir.
	#
	hefst = models.DateTimeField()
	lykur = models.DateTimeField()

	class Meta:
		verbose_name_plural = 'timabil'

	def __str__(self):
		return '%s-%s %s' % (self.hefst.strftime('%H'), self.lykur.strftime('%H'), self.hefst.strftime("%Y.%m.%d"))

	def dags(self):
		return self.hefst.date()

	def skraningar(self):
		skraningar = []
		for vakt in Vakt.objects.filter(timabil=self):
			for skraning in Skraning.objects.filter(vakt=vakt):
				skraningar.append(skraning)
		return len(skraningar)

	def lagmark(self):
		lagmark = 0
		for vakt in Vakt.objects.filter(timabil=self):
			lagmark += vakt.lagmark
		return lagmark

	def litur(self):
		lagmark = self.lagmark()
		if lagmark != 0:
			hlutfall = 255 * self.skraningar() / lagmark
			if hlutfall != 255:
				litur = 'rgb(255,'+str(round(hlutfall))+','+str(round(hlutfall))+')'
			else:
				litur = 'green'
		else:
			litur = 'white'

		return litur

class Starfsstod(models.Model):
	# Nafn sölustaðar eða verkefnis. Dæmi: M6, Grjótháls, bílstjórar,
	# stjórnstöð...
	#
	nafn = models.CharField(max_length=32)

	class Meta:
		verbose_name_plural = 'starfsstöðvar'

	def skraningar(self):
		return Vakt.objects.filter(starfsstod=self).count()

	def lagmark(self):
		lagmark = 0
		for vakt in Vakt.objects.filter(starfsstod=self):
			lagmark += vakt.lagmark
		return lagmark

	def __str__(self):
		return self.nafn

class Tegund(models.Model):
	# Tegund vaktar. Dæmi: sala, næturvakt, undirbúningur, stuðningur.
	#
	nafn = models.CharField(max_length=32)

	class Meta:
		verbose_name_plural = 'tegundir'

	def __str__(self):
		return self.nafn

class Vakt(models.Model):

	# Vaktin hefur ákveðið tímabil, dagsetningu og er úthlutað ákveðinn
	# sölustað erða verkefni (Staða).
	timabil = models.ForeignKey(Timabil)
	starfsstod = models.ForeignKey(Starfsstod)

	# Hver vakt hefur ákveðið lágmark sem við þurfum að manna og ákveðið hámark
	# sem við þurfum alls ekki að fara yfir.
	lagmark = models.SmallIntegerField()
	hamark = models.SmallIntegerField(null=True,blank=True)

	# Hver vakt hefur einnig ákveðna tegund.
	tegund = models.ForeignKey(Tegund)

	class Meta:
		verbose_name_plural = 'vaktir'

	def __str__(self):
		return '%s (%s %s) [%s-%s] %s' % (self.starfsstod, self.timabil.hefst.strftime('%D'), self.timabil, str(self.lagmark), str(self.hamark), self.tegund)

class Felagi(models.Model):
	# Viö höldum utan um félagana sem skrá sig.
	#
	kennitala = models.IntegerField()
	nafn = models.CharField(max_length=32)
	simi = models.IntegerField()
	netfang = models.CharField(max_length=32)

	# Félagar geta skráð "Kannski" vaktir (sjá skráningu). Hér geta þeir
	# tilgreint hámakrsfjölda vakta sem þeir eru tilbúnir til að sinna.
	geta = models.PositiveSmallIntegerField(null=True,blank=True)

	class Meta:
		verbose_name_plural = 'felagar'

	def __str__(self):
		return self.nafn

class Loggur(models.Model):
	# Hér loggum við skráningu félaga eða breytingar á skráningu þeirra í
	# gegnum viðmótið.

	timastimpill = models.DateTimeField(auto_now_add=True)
	# Ef skráningin er gerð úr umsjónarkerfinu, loggum við hver gerir hana:
	notandi = models.ForeignKey(User, related_name='loggar', null=True,blank=True)

	class Meta:
		verbose_name_plural = 'loggar'

	def __str__(self):
		return self.timastimpill.strftime('%D')

class Skraning(models.Model):
	# Hér eru félagar skráðir á vaktir. Hver félagi getur verið með fleiri
	# en eina vakt og er þá með þann fjölda skráninga.
	#
	felagi = models.ForeignKey(Felagi, related_name='skraningar')
	vakt = models.ForeignKey(Vakt, related_name='skraningar')

	#timastimpill = models.DateTimeField(auto_now_add=True)
	#breytistimpill = models.DateTimeField(auto_now=True)
	loggur = models.ForeignKey(Loggur, related_name='skraningar')

	# Hver svörun getur verið eitt af:
	SVORUN_VALMOGULEIKAR = (
		(0, 'Nei'),
		(1, 'Já'),
		(2, 'Kannski'),
	)
	#svorun = models.PositiveSmallIntegerField(choices=SVORUN_VALMOGULEIKAR,default=0)

	class Meta:
		verbose_name_plural = 'skraningar'
		unique_together = ( 'felagi', 'vakt' )

	def __str__(self):
		return '%s [%s]: %s' % (self.felagi, self.SVORUN_VALMOGULEIKAR[self.svorun][1], self.vakt.tegund)
