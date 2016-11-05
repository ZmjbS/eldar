from django.shortcuts import render_to_response
from django.shortcuts import render
from vaktir.models import Vakt, Starfsstod, Timabil, Skraning, Tegund, Felagi, Loggur

def dagalisti():
	''' Búum til lista yfir dagana sem vaktirnar ná yfir og skilum í röðuðum lista.
	'''
	dagalisti = []
	for vakt in Vakt.objects.all():
		if vakt.timabil.dags() not in dagalisti:
			dagalisti.append(vakt.timabil.dags())
	dagalisti.sort()

	return dagalisti

def starfsstodvayfirlit():
	'''
	Búum til yfirlit yfir vaktir starfsstöðvanna til að senda á yfirlitið.
	Taflan hefur raðir eftir starfsstöðvum, nema haus hennar inniheldur
	samantekta mönnun og þörf á mönnun.
	Hver dálkur inniheldur eitt tímabil og í röðum starfsstaðanna eru .
	'''
	#TODO: Klára lýsinguna

	timabilin = Timabil.objects.all().order_by('hefst')

	starfsstodvalisti = []

	# Förum í gegnum starfsstöðvarnar og búum til lista sem samsvarar tímabilunum í timabil
	for starfsstod in Starfsstod.objects.all():
		vaktir = []
		for timabilid in timabilin:
			# Bætum vaktinni við listann ef hún er til:
			try:
				vaktir.append(Vakt.objects.get(timabil=timabilid, starfsstod=starfsstod))
			# Annars fer bara autt stak í listann:
			except:
				vaktir.append('')
		starfsstodvalisti.append({ 'starfsstod': starfsstod, 'vaktir': vaktir, }) 

	# Finnum út hversu mörg tímabil eru á hverjum degi:
	dagatimabil = []
	for dagur in dagalisti():
		fjoldi = Timabil.objects.filter(
			hefst__day=dagur.day,
			hefst__month=dagur.month,
			hefst__year=dagur.year
			).count()
		print(fjoldi)
		dagatimabil.append({ 'dagur': dagur, 'fjoldi_timabila': fjoldi, })

	gogn_til_snidmats = {
		'starfsstodvalisti': starfsstodvalisti,
		'timabilin': timabilin,
		'dagar': dagalisti(),
		'dagatimabil': dagatimabil,
	}

	return gogn_til_snidmats

def skraning(request):
	"""
	Skilar viðmóti sem býður notanda upp á að skrá sig. Til dæmis svæði
	fyrir kennitölu og lág tafla yfir vaktir á tímana.
	"""

	gogn_til_snidmats = starfsstodvayfirlit()

	return render(request, 'vaktir/skraning.html', starfsstodvayfirlit() )

def skra(request):
	""" Tekur við POST beiðni, vistar skráninguna og skilar upplýsingum til notanda um hana.
	"""
	nafn = request.POST.get('nafn')
	simi = request.POST.get('simi')
	netfang = request.POST.get('netfang')
	athugasemd = request.POST.get('athugasemd')

	print(request.POST)

	felagi, felagi_smidadur = Felagi.objects.get_or_create(netfang=netfang, defaults={ 'nafn': nafn, 'simi': simi, })
	# Debug:
	if felagi_smidadur:
		print('félagi smíðaður')
	else:
		print('félagi sóttur')
	print(felagi)
	# End debug

	loggur = Loggur.objects.create(athugasemd=athugasemd)

	for vakt_id in request.POST.getlist('vaktir',''):
		#print(vakt_id)
		vakt = Vakt.objects.get(pk=vakt_id)
		#print(vakt)
		#skraning, buin_til = Skraning.object.get_or_create(felagi=felagi,vakt=vakt,svorun=1)
		Skraning.objects.get_or_create(felagi=felagi,vakt=vakt,loggur=loggur)

	gogn_til_snidmats = starfsstodvayfirlit()
	gogn_til_snidmats['felagi'] = felagi
	gogn_til_snidmats['loggur'] = loggur
	return render(request, 'vaktir/skraning.html', gogn_til_snidmats)

def fletta_upp(request):
	return render(request, 'vaktir/skraning.html',)

def umsjon(request):
	""" Skilar bara yfirliti yfir vaktastöðuna.
	"""
	return render_to_response('vaktir/yfirlit.html', starfsstodvayfirlit() )

# TODO: Seinni tíma verk...
#def smidi(request):
#
#	gogn_til_snidmats = starfsstodvayfirlit()
#	gogn_til_snidmats['tegundalisti'] = Tegund.objects.all()
#
#	return render(request, 'vaktir/skraning.html', gogn_til_snidmats)
