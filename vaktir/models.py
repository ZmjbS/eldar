from django.db import models

class Timabil(models.Model):
	# Hver vakt hefur sitt tímabil. Til að einfalda uppsetningu vakta eru
	# skilgreind nokkur tímabil og svo vöktunum úthlutað þeim. Þannig er líka
	# auðveldara að hnika til vöktum; skeyta tveimur saman eða stytta vaktir.
	#
	hefst = models.TimeField()
	lykur = models.TimeField()

	class Meta:
		verbose_name_plural = 'timabil'

	def __str__(self):
		return '%s-%s' % (self.hefst.strftime('%H'), self.lykur.strftime('%H'))

class Starfsstod(models.Model):
	# Nafn sölustaðar eða verkefnis. Dæmi: M6, Grjótháls, bílstjórar,
	# stjórnstöð...
	#
	nafn = models.CharField(max_length=32)

	class Meta:
		verbose_name_plural = 'stodur'

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
	dags = models.DateField()
	starfsstod = models.ForeignKey(Starfsstod)

	# Hver vakt hefur ákveðið lágmark sem við þurfum að manna og ákveðið hámark
	# sem við þurfum alls ekki að fara yfir.
	lagmark = models.SmallIntegerField()
	hamark = models.SmallIntegerField()

	# Hver vakt hefur einnig ákveðna tegund.
	tegund = models.ForeignKey(Tegund)

	class Meta:
		verbose_name_plural = 'vaktir'

	def __str__(self):
		return '%s (%s %s) [%s-%s] %s' % (self.starfsstod, self.dags.strftime('%D'), self.timabil, str(self.lagmark), str(self.hamark), self.tegund)

class Felagi(models.Model):
	# Viö höldum utan um félagana sem skrá sig.
	#
	kennitala = models.IntegerField()
	nafn = models.CharField(max_length=32)
	simi = models.IntegerField()
	netfang = models.CharField(max_length=32)

	# Félagar geta skráð "Kannski" vaktir (sjá skráningu). Hér geta þeir
	# tilgreint hámakrsfjölda vakta sem þeir eru tilbúnir til að sinna.
	geta = models.PositiveSmallIntegerField(blank=True)

	class Meta:
		verbose_name_plural = 'felagar'

class Skraning(models.Model):
	# Hér eru félagar skráðir á vaktir. Hver félagi getur verið með fleiri ein
	# eina vakt og er þá með þann fjölda skráninga.
	#
	felagi = models.ForeignKey(Felagi, related_name='skraningar')
	vakt = models.ForeignKey(Vakt, related_name='skraningar')

	# Hver svörun getur verið eitt af:
	SVORUN_VALMOGULEIKAR = (
		(0, 'Nei'),
		(1, 'Já'),
		(2, 'Kannski'),
	)
	svorun = models.PositiveSmallIntegerField(choices=SVORUN_VALMOGULEIKAR,default=0)

	class Meta:
		verbose_name_plural = 'skraningar'
