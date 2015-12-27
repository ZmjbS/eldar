from django.db import models

class Skoteldur(models.Model):
	# Vörunúmer er sett saman úr þremur númerum:
	#   aavvrr
	# þar sem aa er árgerðin (t.d. 08 fyrir 2008), vv er vörugerðin (sjá neðar) og rr er raðnúmer þess skotelds þeirrar gerðar þess árs.
	argerd = models.SmallIntegerField()
	vorugerd = models.SmallIntegerField()
	radnumer = models.SmallIntegerField()

	# Stutt nafn skotelds er eitthvað sem passar auðveldar á verðmiða.
	fulltnafn = models.CharField(max_length=64)
	stuttnafn = models.CharField(max_length=64)

	# Verð vörunnar.
	verd = models.SmallIntegerField()

	# Staða vörunnar eins og er.
	stada = models.SmallIntegerField()
	# Ný vara sem bætist við lagerinn. Þetta þarf að bæta við stöðuna og endurstilla við upphaf sölu.
	nytt = models.SmallIntegerField(default=0)

	# Lýsing á vörunni og aðrar athugasemdir eins og hvernig hún er að reynast í sölu, hvort kaupa eigi meira af henni eða hætt sé að taka hana inn.
	lysing = models.TextField(blank=True)
	athugasemdir = models.TextField(blank=True)

	class Meta:
		verbose_name_plural = 'skoteldar'
