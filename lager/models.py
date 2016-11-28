# coding=utf-8
from django.db import models

from vaktir.models import Starfsstod

import math

class Vara(models.Model):
	'''
	Hver vara hefur sér verð sem er geymt í sér hlut til að geta safnað upp
	verðsögu vörunnar.

	Vörur hafa ákveðna stöðu en ennfremur er hægt að tengja einingar við vöruna
	til að tilgreina staðsetningu þeirra til að auðvelda vörutalningu.
	'''

	# Vörunúmer er sett saman úr þremur númerum:
	#   aavvrr
	# þar sem aa er árgerðin (t.d. 08 fyrir 2008), vv er vörugerðin
	# (sjá neðar) og rr er raðnúmer þess skotelds þeirrar gerðar
	# þess árs.
	argerd = models.SmallIntegerField()
	vorugerd = models.SmallIntegerField()
	radnumer = models.SmallIntegerField()

	# Kassanúmerið er vörunúmer framleiðanda.
	kassanumer = models.CharField(max_length=8, blank=True)

	# Stutt nafn skotelds er eitthvað sem passar auðveldar á verðmiða.
	fulltnafn = models.CharField(max_length=64)
	stuttnafn = models.CharField(max_length=64, blank=True)

	# Staða vörunnar eins og er.
	# TODO: Kannski bara sleppa þessu í stað Eining-class-ans og fallsins
	# að neðan.
	# Eða nota hvort tveggja ... Þessi staða er þá fyrir smærri einingar
	# sem en hitt fyrir óopnaða kassa ... eða þá að þetta sé fyrir smádót
	# en Eining fyrir stærri einingar sem mögulega virkjast með því að
	# setja þetta sem 0, -1, eða 99999.
	stada = models.SmallIntegerField(null=True, blank=True)

	# Ný vara sem bætist við lagerinn. Þetta þarf að bæta við stöðuna og
	# endurstilla við upphaf sölu.
	nytt = models.SmallIntegerField(null=True, blank=True)

	# Lýsing á vörunni og aðrar athugasemdir eins og hvernig hún er að
	# reynast í sölu, hvort kaupa eigi meira af henni eða hætt sé að taka
	# hana inn.
	lysing = models.TextField(blank=True)
	athugasemdir = models.TextField(blank=True)

	def vorunumer(self):
		def nullfyllt(tala, saeti):
			if tala < 10:
				return '0'+str(tala)
			else:
				return str(tala)

		return nullfyllt(self.argerd,2)   +'-'+ \
			   nullfyllt(self.vorugerd,2) +'-'+ \
			   nullfyllt(self.radnumer,2)

	def __str__(self):
		return self.vorunumer() +' '+ self.fulltnafn+ ' (' + str(self.stada) + ')'
	def verd(self):
		print('halló')
		print(Verd.objects.filter(vara=self).latest().smasoluverd)
		return Verd.objects.filter(vara=self).latest()

	# TODO: Óprófað!!!
	#def stada(self, starfsstod):
	#	einingar = Eining.objects.filter(vara=self, starfsstod=starfsstod)
	#	return einingar.count()

	# TODO: Óprófað!!!
	#def magn(self, starfsstod):
	#	return 3		

	class Meta:
		verbose_name_plural = 'vörur'

# Þetta er bara pæling: Að hafa hverja einingu sér svo hægt sé að gefa henni staðsetningu. Ef við ætlum að vera með bretti eyrnamerkt búðum á milli ára væri ágætt að hafa yfirlit yfir hvar hver vara sé.
# Þetta gæti líka auðveldað uppgjör búða eftir hvern dag.
# Við gætum líka breytt þessu í kerfi þar sem gæti tekið við af Trello og þar sem við höfum yfirlit yfir hvar hver vara er á leið sinni frá lager til búðar.
#class Eining(models.Model):
#	vara = models.ForeignKey(Vara)
#	seljast_fyrir = models.SmallIntegerField()
#	starfsstod = models.ForeignKey(Starfsstod)
#
#	class Meta:
#		verbose_name_plural = 'einingar'

# Eða þetta: Að vera með sölustaðarlagertalningu þannig að hver sölustaður hefur sér fjölda og svo búum við bara til þægilegt viðmót til að færa vöru á milli...
class Bunki(models.Model):
	'''
	Hver bunki inniheldur eina ákveðna vöru á ákveðnum stað eða í flutningi
	á ákveðnu tæki og gerir kleift að fylgja eftir hversu mikið er til af
	hverri vöru og hvar hún er.
	'''
	vara = models.ForeignKey(Vara)
	magn = models.SmallIntegerField()
	
	# Ef bunkinn er í flutning er starfsstöððin tóm og varan sett á ákvðinn
	# flutningsaðila. Þá má t.a.m. tilgreina sem A, B, C eða A1, A2, C1.
	starfsstod = models.ForeignKey(Starfsstod, blank=True)

	# Ártalið sem varan á að seljast á í síðasta lagi.
	seljast_fyrir = models.SmallIntegerField(blank=True)

	
	flutningur = models.CharField(max_length=2)

	def __str__(self):
		return self.vara + str(self.magn)

	class Meta:
		verbose_name_plural = 'bunkar'

class Verd(models.Model):
	'''
	Verð tilgreinir innkaups- og smásöluverð vöru, og dagsetninguna sem
	verðið tekur gildi. Verð eru svo tengd vörum svo verðsaga hverrar vöru
	er geymd.
	'''
	innkaupsverd = models.IntegerField(null=True, blank=True)
	smasoluverd = models.IntegerField(null=True, blank=True)
	vara = models.ForeignKey(Vara)
	dags = models.DateField()

	class Meta:
		verbose_name_plural = 'verð'
		get_latest_by = 'dags'
