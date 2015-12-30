from django.shortcuts import render_to_response
from vaktir.models import Vakt, Starfsstod, Timabil, Skraning

def yfirlit(request):
	
	""" Búum til yfirlit yfir vaktir og skráningar á þær """

	# Búum til lista yfir dagana sem vaktirnar ná yfir.
	dagalisti = []
	for vakt in Vakt.objects.all():
		if vakt.dags not in dagalisti:
			dagalisti.append(vakt.dags)
	print(dagalisti)
	dagalisti.sort()
	print(list(reversed(dagalisti)))
	print(type(dagalisti))

	timabilalisti = Timabil.objects.all()

	starfsstodvarlisti = Starfsstod.objects.all()

	starfsstodvar = {}
	for starfsstod in Starfsstod.objects.all():
		print(starfsstod)
		#dagar = {}
		dagar = []
		for dagur in dagalisti:
			print(dagur)
			timabil = {}
			for timabilid in timabilalisti:
				try:
					vaktin = Vakt.objects.get(dags=dagur,starfsstod=starfsstod,timabil=timabilid)
					#print(vaktin)
					skraningar = Skraning.objects.filter(vakt=vaktin)
	#				print(skraningar)
				except:
					vaktin =""
					skraningar = []
				timabil.update({ timabilid: { 'vaktin': vaktin, 'skraningar': skraningar, }} )
			#dagar.update({ dagur: timabil, })
			dagar.append(timabil)
		starfsstodvar.update({ starfsstod: dagar, })

	return render_to_response('vaktir/yfirlit.html', { 'dagalisti': dagalisti, 'timabilalisti': timabilalisti, 'starfsstodvar': starfsstodvar, })
