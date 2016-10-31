from django.shortcuts import render
from lager.models import Vara

def yfirlit(request):
	vorur = Vara.objects.all()

	verdmidar(vorur)

	return render(request, 'lager/yfirlit.html', { 'vorur': vorur, })

def verdmidar(vorur):
	""" Býr til PDF skjal af verðmiðum úr lista af Vörum.
	"""
	import labels
	from reportlab.graphics import shapes
	from reportlab.pdfbase.pdfmetrics import stringWidth

	# Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 8 rows of
	# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
	# automatically calculated.
	specs = labels.Specification(210, 297, 2, 8, 90, 25, corner_radius=2)

	# Create a function to draw each label. This will be given the ReportLab drawing
	# object to draw on, the dimensions (NB. these will be in points, the unit
	# ReportLab uses) of the label, and the object to render.
	def draw_label(label, width, height, vara):

		textastaerd = 32
		nafnbreidd = stringWidth(vara.fulltnafn, "Helvetica", textastaerd)
		while nafnbreidd > width-4:
			textastaerd *= 0.95
			nafnbreidd = stringWidth(vara.fulltnafn, "Helvetica", textastaerd)

		nafnbreidd = stringWidth(vara.fulltnafn, "Helvetica", textastaerd)
		label.add(shapes.String((width-nafnbreidd)/2, height-32-16, str(vara.fulltnafn), fontName="Helvetica", fontSize=textastaerd))

		label.add(shapes.String(2, 2, str(vara.verd().smasoluverd)+' kr.', fontName="Helvetica", fontSize=16))
		label.add(shapes.String(width-2, 2, str(vara.vorunumer()), fontName="Helvetica", fontSize=16,textAnchor="end"))

	# Create the sheet.
	#sheet = labels.Sheet(specs, draw_label, border=False)
	sheet = labels.Sheet(specs, draw_label)

	# Add a couple of labels.
	for vara in vorur:
		sheet.add_label(vara)
		print(vara.verd())
		#print(vara.verd)

	# Save the file and we are done.
	sheet.save('basic.pdf')
	print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))
