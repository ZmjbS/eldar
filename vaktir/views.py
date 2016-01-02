from django.shortcuts import render_to_response
from vaktir.models import Vakt, Starfsstod, Timabil, Skraning, Tegund, Felagi

def starfsstodvayfirlit():

	""" Búum til yfirlit yfir vaktir og skráningar á þær """

	# Búum til lista yfir dagana sem vaktirnar ná yfir.
	#
	dagalisti = []
	for vakt in Vakt.objects.all():
		if vakt.dags not in dagalisti:
			dagalisti.append(vakt.dags)
	dagalisti.sort()

	timabilalisti = Timabil.objects.all()

	# Þessi listi daga og tímabila er aðallega gagnlegur til að reikna upp
	# heildarskránignar yfir það tímabil og heildarlágmark sem þarf fyrir allt
	# tímabilið.
	#
	print(timabilalisti)
	dagstimabil = []
	for dagur in dagalisti:
		tbl = []
		for tb in timabilalisti:
			tbl.append( { 'timabil': tb, 'skraningar': tb.skraningar(dagur), 'lagmark': tb.lagmark(dagur), } )
		dagstimabil.append(tbl)
	print(dagstimabil)

	""" Útbúum nokkurra laga lista af orðabókum til að birta töflu á þessu
	sniði:
	             | Dagur 1         | Dagur 2         ...
	starfsstaður | tb1 | tb2 | tb3 | tb1 | tb2 | tb3 ...

	Því þurfum við að búa til þetta ferlíki:
	  [ starfsstod, dagar:[ timabilin:[ timabilid, vaktin, skraningar:[] ] ] ]
	"""

	starfsstodvarlisti = Starfsstod.objects.all()

	starfsstodvar = []
	for starfsstod in Starfsstod.objects.all():

		# Setjum daga í lista svo hægt sé að lykkja í gegnum þá í réttri röð.
		dagar = []
		for dagur in dagalisti:
			
			# Fyrir hvern dag eru nokkur tímabil...
			timabil = []
			for timabilid in timabilalisti:
				try:
					# Það er bara ein vakt fyrir hvert tímabil á hverri
					# starfsstöð.
					vaktin = Vakt.objects.get(
						dags=dagur,
						starfsstod=starfsstod,
						timabil=timabilid)
					# Sækjum allar skráningarnar sem komnar eru.
					skraningar = Skraning.objects.filter(vakt=vaktin)
				except:
					# Ef engin er vaktin setjum við bara inn tóm gildi.
					vaktin =""
					skraningar = []
				# Stingum nú vaktinni og skráningunum inn í 
				timabil.append({ 'vaktin': vaktin, 'skraningar': skraningar, })
			dagar.append( { 'timabil': timabil, } )
		starfsstodvar.append( { 'starfsstod': starfsstod, 'dagar': dagar, })

	felagalisti = Felagi.objects.all()
	
	gogn_til_snidmats = {
		'dagalisti': dagalisti,
		'timabilalisti': timabilalisti,
		'starfsstodvar': starfsstodvar,
		'dagstimabil': dagstimabil,
		'felagalisti': felagalisti,
		}
	return gogn_til_snidmats

def yfirlit(request):
	""" Skilar bara yfirliti yfir vaktastöðuna
	"""
	return render_to_response('vaktir/yfirlit.html', starfsstodvayfirlit() )

def skraning(request):
	""" Skilar viðmóti sem býður notanda upp á að skrá sig. Til dæmis svæði fyrir kennitölu og lág tafla yfir vaktir á tímanakkkk
	"""
	return render_to_response('vaktir/yfirlit.html', starfsstodvayfirlit() )

def smidi(request):

	starfsstodvarlisti = Starfsstod.objects.all()
	dagalisti = []
	for vakt in Vakt.objects.all():
		if vakt.dags not in dagalisti:
			dagalisti.append(vakt.dags)
	dagalisti.sort()
	timabilalisti = Timabil.objects.all()

	tegundalisti = Tegund.objects.all()

	# Hérna væri gott að taka út þær starfsstöðvar sem þegar er búið að skrá vaktir á, eða möndla það þannig að við fá... ah, hvað með að búa bara til form á vaktalausu dagana? ... ah, nei, við viljum náttúrulega líka geta breytt hinum.
	# Já, kannski er bara best að vera með alla púllíuna/töfluna og bæta við edit-pakka á þessu view-i...

	gogn_til_snidmats = {
		'dagalisti': dagalisti,
		'timabilalisti': timabilalisti,
		#'starfsstodvar': starfsstodvar,
		'starfsstodvarlisti': starfsstodvarlisti,
		'tegundalisti': tegundalisti,
		}
	return render_to_response('vaktir/smidi.html', gogn_til_snidmats)
