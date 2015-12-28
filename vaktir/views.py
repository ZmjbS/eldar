from django.shortcuts import render_to_response
from vaktir.models import Vakt, Starfsstod, Timabil, Skraning

def yfirlit(request):
	
	""" Búum til yfirlit yfir vaktir og skráningar á þær """

	# Búum til lista yfir dagana sem vaktirnar ná yfir.
	dagalisti = []
	for vakt in Vakt.objects.all():
		if vakt.dags not in dagalisti:
			dagalisti.append(vakt.dags)
		
	# Förum nú í gegnum dagana einn af öðrum og bætum við vöktum og skráningum
	# á þær vaktir.
	dagar = {}
	for dagur in dagalisti:
		starfsstodvar = {}
		for starfsstod in Starfsstod.objects.all():
			timabil = {}
			for timabilid in Timabil.objects.all():
				#vaktir = Vakt.objects.filter(\
				#	dags=dagur,\
				#	starfsstod=starfsstod,\
				#	timabil=timabilid,\
				#)
				skraningar = []
				try:
					vaktin = Vakt.objects.get(dags=dagur,starfsstod=starfsstod,timabil=timabilid)
					print(vaktin)
					skraningar = Skraning.objects.filter(vakt=vaktin)
					print(skraningar)
				except:
					print('Engin vakt skráð á þetta tímabil.')
				#print(vaktir)
				#skraningar = {}
				#for vakt in vaktir:
				#	skraningar.update(\
				#		{ vakt: Skraning.objects.filter(vakt=vakt) }\
				#	)

				#skraningar = []
				#for vakt in vaktir:
				#	skraningar.append(Skraning.objects.filter(vakt=vakt))
				#timabil.update({ timabilid: { 'vaktin': vaktir, 'skraningar': skraningar, } })
				timabil.update({ timabilid: skraningar, })
			#print(timabil)
			starfsstodvar.update({ starfsstod: timabil, })
		#print(starfsstodvar)
		dagar.update({ dagur: starfsstodvar, })

	#print(dagar)

	#	# Tilgreinum hverjir eru búnir að skrá sig á vaktir þessa dags.
	#	vaktaskraning = {}
	#	timabil = {}
	#	for vakt in Vakt.objects.filter(dags=dagur):
	#		timabil.update({
	#		vaktaskraning.update({ vakt: vakt.skraningar.all(), })
	#	# Tilgreinum svo hvaða vaktir eru á þessum degi.
	#	#dagavaktir.update({ dagur: vaktaskraning, })

	return render_to_response('vaktir/yfirlit.html', { 'dagar': dagar, })
