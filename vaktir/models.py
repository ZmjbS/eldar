# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
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

	def vaktaskraningar(self):
		vaktaskraningar = []
		for vakt in Vakt.objects.filter(timabil=self):
			for vs in Vaktaskraning.objects.filter(vakt=vakt):
				vaktaskraningar.append(vs)
		return len(vaktaskraningar)

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

@python_2_unicode_compatible
class Starfsstod(models.Model):
	# Nafn sölustaðar eða verkefnis. Dæmi: M6, Grjótháls, bílstjórar,
	# stjórnstöð...
	#
	nafn = models.CharField(max_length=32)
	hamark = models.IntegerField()
	solustadur = models.BooleanField()

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

@python_2_unicode_compatible
class Tegund(models.Model):
	# Tegund vaktar. Dæmi: sala, næturvakt, undirbúningur, stuðningur.
	#
	nafn = models.CharField(max_length=32)

	class Meta:
		verbose_name_plural = 'tegundir'

	def __str__(self):
		return self.nafn

@python_2_unicode_compatible
class Vakt(models.Model):

	# Vaktin hefur ákveðið tímabil, dagsetningu og er úthlutað ákveðinn
	# sölustað erða verkefni (Staða).
	timabil = models.ForeignKey(Timabil)
	starfsstod = models.ForeignKey(Starfsstod, related_name='vaktir')

	# Hver vakt hefur ákveðið lágmark sem við þurfum að manna og ákveðið hámark
	# sem við þurfum alls ekki að fara yfir.
	lagmark = models.SmallIntegerField()
	hamark = models.SmallIntegerField(null=True,blank=True)

	# Hver vakt hefur einnig ákveðna tegund.
	tegund = models.ForeignKey(Tegund)

	def vaktaskraningar(self):
		'''
		Þar sem vaktaskráningar fyrir ákveðna vakt eru ekki endilega í
		nýjustu skráningunni þurfum við að búa til sér lista fyrir
		þetta.
		'''
		vs_listi = []
		for vs in Vaktaskraning.objects.filter(vakt=self):
			# Bætum vaktaskráningunni við ef hún er í nýjustu skráningu félagans.
			if vs.skraning == Skraning.objects.filter(felagi=vs.skraning.felagi).latest('timastimpill'):
				vs_listi.append(vs)
		return vs_listi

	# def skradir(self):
	# 	return len(self.vaktaskraningar())

	class Meta:
		verbose_name_plural = 'vaktir'

	def __str__(self):
		return '%s (%s %s) [%s-%s] %s' % (self.starfsstod, self.timabil.hefst.strftime('%D'), self.timabil, str(self.lagmark), str(self.hamark), self.tegund)

@python_2_unicode_compatible
class Felagi(models.Model):
	# Viö höldum utan um félagana sem skrá sig.
	#
	#kennitala = models.IntegerField()
	nafn = models.CharField(max_length=32)
	simi = models.IntegerField()
	netfang = models.CharField(max_length=32)
	adalStarfsstod = models.ForeignKey(Starfsstod)

	def vaktaskraningar(self):
		'''
		Skilar vaktaskráningum nýjustu skráningarinnar
		'''
		skraning = self.skraningar.order_by('-timastimpill')[0]
		vaktaskraningar = Vaktaskraning.objects.filter(skraning=skraning)
		return vaktaskraningar


	class Meta:
		verbose_name_plural = 'felagar'

	def __str__(self):
		return self.nafn

@python_2_unicode_compatible
class Skraning(models.Model):
	'''
	Þegar félagi skráir sig býr hann til skráningu sem núll eða fleiri
	vaktaksráningar hanga við. 

	Notendur geta svo breytt skráningu í gegnum viðmótið og eru þá merktir
	við skráninguna.
	'''

	felagi = models.ForeignKey(Felagi, related_name='skraningar')
	timastimpill = models.DateTimeField(auto_now_add=True, db_index=True)

	# Ef skráningin er gerð úr umsjónarkerfinu, loggum við hver gerir hana:
	notandi = models.ForeignKey(User, related_name='skraningar', null=True,blank=True)

	# Við hvern logg má bæta athugasemd:
	athugasemd = models.TextField(null=True,blank=True)

	
	# TODO: Enn sem komið er er skráning ígildi staðfestingar á vakt. Það
	# væri hins vegar kostur að gefa möguleika á að merkja vaktir "kannski"
	# og þá einnig fjölda vakta sem viðkomandi er tilbúinn til að sinna.
	# Félagi með sveigjanleika getur t.a.m. mætt á 8 vaktir en hefur ekki
	# getu á að mæta í fleiri en 3. Þá væru þessar átta skráðar sem
	# "kannski" og í skráningunni "geta" hans skráð sem þrjár vaktir.
	#
	# Félagar geta skráð "Kannski" vaktir (sjá skráningu). Hér geta þeir
	# tilgreint hámakrsfjölda vakta sem þeir eru tilbúnir til að sinna.
	# geta = models.PositiveSmallIntegerField(null=True,blank=True)

	class Meta:
		verbose_name_plural = 'skráningar'

	def __str__(self):
		return self.timastimpill.strftime('%D')

@python_2_unicode_compatible
class Vaktaskraning(models.Model):
	# Hér eru félagar skráðir á vaktir. Hver félagi getur verið með fleiri
	# en eina vakt og er þá með þann fjölda skráninga.
	#
	felagi = models.ForeignKey(Felagi, related_name='felagi')
	# Vaktaskráningar fá ekki related_name vegna þess að sumar vaktanna
	# tilheyra eldri skráningum sem eru ekki lengur gildar.
	vakt = models.ForeignKey(Vakt)
	skraning = models.ForeignKey(Skraning, related_name='vaktaskraning')

	# TODO: Enn sem komið er er skráning ígildi staðfestingar á vakt. Það
	# væri hins vegar kostur að gefa möguleika á að merkja vaktir "kannski"
	# og þá einnig fjölda vakta sem viðkomandi er tilbúinn til að sinna.
	# Félagi með sveigjanleika getur t.a.m. mætt á 8 vaktir en hefur ekki
	# getu á að mæta í fleiri en 3. Þá væru þessar átta skráðar sem
	# "kannski" og í skráningunni "geta" hans skráð sem þrjár vaktir.
	#
	# Hver svörun getur verið eitt af:
	#SVAR_VALMOGULEIKAR = (
	#	(1, 'Já'),
	#	(2, 'Kannski'),
	#)
	#svar = models.PositiveSmallIntegerField(choices=SVORUN_VALMOGULEIKAR,default=1)

	class Meta:
		verbose_name_plural = 'vaktaskráningar'
		#unique_together = ( 'felagi', 'vakt' )

	def __str__(self):
		return '%s: %s' % (self.felagi, self.vakt.tegund)
