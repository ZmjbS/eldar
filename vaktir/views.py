from django.shortcuts import render_to_response
from vaktir.models import Vakt, Starfsstod, Timabil, Skraning

def yfirlit(request):
	
	""" Búum til yfirlit yfir vaktir og skráningar á þær """

	# Búum til lista yfir dagana sem vaktirnar ná yfir.
	dagalisti = []
	for vakt in Vakt.objects.all():
		if vakt.dags not in dagalisti:
			dagalisti.append(vakt.dags)
	dagalisti.sort()

	timabilalisti = Timabil.objects.all()

	starfsstodvarlisti = Starfsstod.objects.all()

	""" Útbúum djúpa blöndu orðabóka og lista. Við ætlum að búa til töflu á
	þessu sniði:
	             | Dagur 1         | Dagur 2         ...
	starfsstaður | tb1 | tb2 | tb3 | tb1 | tb2 | tb3 ...

	Því þurfum við að búa til þetta ferlíki:
	  { starfsstod: { [ { tímabil: { 'vakt', 'skraning' } } ] } }
	"""

	starfsstodvar = {}
	for starfsstod in Starfsstod.objects.all():

		# Setjum daga í lista svo hægt sé að lykkja í gegnum þá í réttri röð.
		dagar = []
		for dagur in dagalisti:
			
			# Hvert stak í dagalistanum mun innihalda orðabók sem í er:
			# . vaktin
			# . listi af skráningunum
			timabil = {}
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

				vaktskraning = { 'vaktin': vaktin, 'skraningar': skraningar, }
				timabil.update({ timabilid: vaktskraning })
			dagar.append(timabil)
		starfsstodvar.update({ starfsstod: dagar, })

	gogn_til_snidmats = {
		'dagalisti': dagalisti,
		'timabilalisti': timabilalisti,
		'starfsstodvar': starfsstodvar,
		}
	return render_to_response('vaktir/yfirlit.html', gogn_til_snidmats)
