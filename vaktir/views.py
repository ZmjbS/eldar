# coding=utf-8
from django.shortcuts import render_to_response
from django.shortcuts import render
from vaktir.models import Vakt, Starfsstod, Timabil, Vaktaskraning, Tegund, Felagi, Skraning
from django.db import connection
import logging, logging.config
try:
	from future_builtins import zip
except ImportError: # not 2.6+ or is 3.x
	try:
		from itertools import izip as zip # < 2.5 or 3.x
	except ImportError:
		pass
from django.db.models import F, Sum, Prefetch


logger = logging.getLogger('django')

def query_to_dicts(query_string, *query_args):
	"""Run a simple query and produce a generator
	that returns the results as a bunch of dictionaries
	with keys for the column values selected.
	"""
	cursor = connection.cursor()
	cursor.execute(query_string, query_args)
	col_names = [desc[0] for desc in cursor.description]
	while True:
		row = cursor.fetchone()
		if row is None:
			break
		row_dict = dict(zip(col_names, row))
		yield row_dict
	return

def dagalisti():
	''' Búum til lista yfir dagana sem vaktirnar ná yfir og skilum í röðuðum lista.
	'''

	with connection.cursor() as cursor:
		cursor.execute("select date(hefst) as day from vaktir_timabil GROUP BY date(hefst) ORDER BY date(hefst)")
		row = cursor.fetchall()

	return row
	# dagalisti = []
	# for vakt in Vakt.objects.all():
	# 	if vakt.timabil.dags() not in dagalisti:
	# 		dagalisti.append(vakt.timabil.dags())
	# dagalisti.sort()

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


	# Förum í gegnum starfsstöðvarnar og búum til lista sem samsvarar tímabilunum í timabil
	# starfsstodvalisti = Starfsstod.objects.all().prefetch_related('vaktir__skraning').annotate(
	# 	lagmark=Sum('vaktir__lagmark'),
	# )

	with connection.cursor() as cursor:
		cursor.execute("""SELECT DISTINCT ON (felagi_id)
				id
			FROM vaktir_skraning vs
			ORDER  BY felagi_id, timastimpill DESC""")
		ids = cursor.fetchall()

	starfsstodvalisti = Starfsstod.objects.all().annotate(
		lagmark=Sum('vaktir__lagmark'),
	).prefetch_related(
		Prefetch('vaktir', queryset=Vakt.objects.all()),
		Prefetch('vaktir__vaktaskraning', queryset=Vaktaskraning.objects.filter(skraning_id__in=ids).select_related('felagi'), to_attr='vaktaskraningar'),
	)

	dagatimabil = query_to_dicts("select date(hefst) as dagur, count(id) as fjoldi_timabila from vaktir_timabil GROUP BY date(hefst) ORDER BY date(hefst)")

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

	if request.method == 'POST':
		print('POST')
		vidbotargogn = skra(request)
	else:
		print('GET')
		vidbotargogn = fletta_upp(request)
		print(vidbotargogn)

	if vidbotargogn:
		for key, val in vidbotargogn.items():
			gogn_til_snidmats[key] = val

	return render(request, 'vaktir/skraning.html', gogn_til_snidmats )

def fletta_upp(request):
	'''
	Skilar upplýsingum um skráningar félaga eftir netfanginu sem gefið er upp.
	'''

	print('hér')
	netfang = request.GET.get('netfang')
	print(netfang)
	if netfang:
		try:
			felagi = Felagi.objects.get(netfang=netfang)
			gogn_til_snidmats = { 'felagi': felagi, }
			return gogn_til_snidmats
		except:
			return None
	else:
		return None

def skra(request):
	""" Tekur við POST beiðni, vistar skráninguna og skilar upplýsingum til notanda um hana.
	"""
	nafn = request.POST.get('nafn')
	simi = request.POST.get('simi')
	simi = ''.join(filter(lambda x: x.isdigit(), simi))
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

	skraning = Skraning.objects.create(felagi=felagi,athugasemd=athugasemd)

	for vakt_id in request.POST.getlist('vaktir',''):
		#print(vakt_id)
		vakt = Vakt.objects.get(pk=vakt_id)
		#print(vakt)
		Vaktaskraning.objects.get_or_create(felagi=felagi,vakt=vakt,skraning=skraning)

	gogn_til_snidmats = starfsstodvayfirlit()
	gogn_til_snidmats['felagi'] = felagi
	gogn_til_snidmats['skraning'] = skraning
	return gogn_til_snidmats

def umsjon(request):
	""" Skilar bara yfirliti yfir vaktastöðuna.
	"""

	gogn_til_snidmats = starfsstodvayfirlit()
	gogn_til_snidmats['skraningar'] = Skraning.objects.all().order_by('-timastimpill')

	return render_to_response('vaktir/yfirlit.html', gogn_til_snidmats )

# TODO: Seinni tíma verk...
#def smidi(request):
#
#	gogn_til_snidmats = starfsstodvayfirlit()
#	gogn_til_snidmats['tegundalisti'] = Tegund.objects.all()
#
#	return render(request, 'vaktir/skraning.html', gogn_til_snidmats)
