from django.db import models

# TODO: er þetta réttur syntax?
from eldar.vaktir import Starfsstod

import math

class Vara(models.Model):
	# Vörunúmer er sett saman úr þremur númerum:
	#   aavvrr
	# þar sem aa er árgerðin (t.d. 08 fyrir 2008), vv er vörugerðin (sjá neðar) og rr er raðnúmer þess skotelds þeirrar gerðar þess árs.
	argerd = models.SmallIntegerField()
	vorugerd = models.SmallIntegerField()
	radnumer = models.SmallIntegerField()

	# Stutt nafn skotelds er eitthvað sem passar auðveldar á verðmiða.
	fulltnafn = models.CharField(max_length=64)
	stuttnafn = models.CharField(max_length=64)

	# Höfum það heldur þannig að hver vara geti haft mörg verð (og svo notum við bara það nýjasta frá hverju ári. Hendum hins vegar ekki hinum heldur búum við bara til verð og tengjum það vöru með ForeignKey
	## Verð vörunnar.
	#verd = models.SmallIntegerField()

	# Staða vörunnar eins og er.

	# TODO: Kannski bara sleppa þessu í stað Eining-class-ans og fallsins að neðan.
	stada = models.SmallIntegerField()

	# Ný vara sem bætist við lagerinn. Þetta þarf að bæta við stöðuna og endurstilla við upphaf sölu.
	nytt = models.SmallIntegerField(default=0)

	# Lýsing á vörunni og aðrar athugasemdir eins og hvernig hún er að reynast í sölu, hvort kaupa eigi meira af henni eða hætt sé að taka hana inn.
	lysing = models.TextField(blank=True)
	athugasemdir = models.TextField(blank=True)

	def __str__(self):
		def nullfyllt(tala, saeti):
			strengur = str(tala)
			lengd = math.floor(math.log10(tala))
			for i in range(saeti-lengd-1):
				strengur = '0'+strengur
			return strengur

		return nullfyllt(self.argerd,2)   +'-'+ \
			   nullfyllt(self.vorugerd,2) +'-'+ \
			   nullfyllt(self.radnumer,2) +' '+ \
			   self.stuttnafn + ' (' + str(self.stada) + ')'

	# TODO: Óprófað!!!
	def stada(self):
		einingar = Eining.objects.filter(vara=self)
		return einingar.count()

	class Meta:
		verbose_name_plural = 'vörur'

# Þetta er bara pæling: Að hafa hverja einingu sér svo hægt sé að gefa henni staðsetningu. Ef við ætlum að vera með bretti eyrnamerkt búðum á milli ára væri ágætt að hafa yfirlit yfir hvar hver vara sé.
# Þetta gæti líka auðveldað uppgjör búða eftir hvern dag.
# Við gætum líka breytt þessu í kerfi þar sem gæti tekið við af Trello og þar sem við höfum yfirlit yfir hvar hver vara er á leið sinni frá lager til búðar.
class Eining(models.Model):
	vara = models.ForeignKey(Vara)
	seljast_fyrir = models.SmallIntegerField()
	stadsetning = models.ForeignKey(Starfsstod)

class Verd(models.Model):
	innkaupsverd = models.SmallIntegerField()
	smasoluverd = models.SmallIntegerField()
	vara = models.ForeignKey(Vara)
	dags = models.DateField()

	class Meta:
		verbose_name_plural = 'verð'
