from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
import vr.models as dbmodels
import datetime


def start(request):
	"""Startseite."""
	if not request.user.is_authenticated():
		return redirect('regionenraten_login')
	aSeite = 0
	if 'seite' in request.GET and request.GET.get('seite'):
		aSeite = int(request.GET.get('seite'))
	getXls = False
	if 'get' in request.GET and request.GET.get('get') == 'xls':
		getXls = True
	aAuswertungen = []
	prev = -1
	next = -1
	maxPerPage = 14
	aAntwortenM = dbmodels.antworten.objects.all().order_by('-spiel__spieler__zeit', 'spiel__zeit')
	aCount = aAntwortenM.count()
	# Seiten
	if getXls:
		import xlwt
		response = HttpResponse(content_type='text/ms-excel')
		response['Content-Disposition'] = 'attachment; filename="regionenraten_' + datetime.date.today().strftime('%Y%m%d') + '.xls"'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('regionenraten')
		row_num = 0
		columns = []
		columns.append(('Nr', 2000))
		columns.append(('Antworten Id', 2000))
		columns.append(('Antworten beispiel', 2000))
		columns.append(('Antworten wiedergaben', 2000))
		columns.append(('Antworten gewOrt', 2000))
		columns.append(('Antworten hochdeutsch', 2000))
		columns.append(('Antworten orf', 2000))
		columns.append(('Antworten pOrt', 2000))
		columns.append(('Antworten aufgefallen', 2000))
		columns.append(('Antworten zeit', 2000))
		columns.append(('Spiel Id', 2000))
		columns.append(('Spiel Zeit', 2000))
		columns.append(('Audiodatei Id', 2000))
		columns.append(('Audiodatei file', 2000))
		columns.append(('Audiodatei ort', 2000))
		columns.append(('Audiodatei benutzt', 2000))
		columns.append(('Spieler Id', 2000))
		columns.append(('Spieler zeit', 2000))
		columns.append(('Spieler geburtsjahr', 2000))
		columns.append(('Spieler gesch', 2000))
		columns.append(('Spieler taetigkeit', 2000))
		columns.append(('Spieler wohnort', 2000))
		columns.append(('Spieler wohnortLeben', 2000))
		columns.append(('Spieler wohnortEltern', 2000))
		columns.append(('Spieler erkannt', 2000))
		columns.append(('Spieler anmerkungen', 2000))
		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num][0], font_style)
		font_style = xlwt.XFStyle()
		font_style_datetime = xlwt.XFStyle()
		font_style_datetime.num_format_str = 'YYYY-MM-DD hh:mm:ss'
		for obj in aAntwortenM:
			row_num += 1
			ws.write(row_num, 0, row_num, font_style)
			ws.write(row_num, 1, obj.pk, font_style)
			ws.write(row_num, 3, obj.beispiel, font_style)
			ws.write(row_num, 4, obj.wiedergaben, font_style)
			ws.write(row_num, 5, str(obj.gewOrt), font_style)
			ws.write(row_num, 6, obj.hochdeutsch, font_style)
			ws.write(row_num, 6, obj.orf, font_style)
			ws.write(row_num, 6, obj.pOrt, font_style)
			ws.write(row_num, 6, obj.aufgefallen, font_style)
			ws.write(row_num, 7, obj.zeit, font_style_datetime)
			ws.write(row_num, 8, obj.spiel.pk, font_style)
			ws.write(row_num, 9, obj.spiel.zeit, font_style_datetime)
			ws.write(row_num, 10, obj.audiodatei.pk, font_style)
			ws.write(row_num, 11, obj.audiodatei.file, font_style)
			ws.write(row_num, 13, str(obj.audiodatei.ort), font_style)
			ws.write(row_num, 17, obj.audiodatei.benutzt, font_style)
			ws.write(row_num, 18, obj.spiel.spieler.pk, font_style)
			ws.write(row_num, 19, obj.spiel.spieler.zeit, font_style_datetime)
			ws.write(row_num, 20, obj.spiel.spieler.geburtsjahr, font_style)
			ws.write(row_num, 21, obj.spiel.spieler.gesch, font_style)
			ws.write(row_num, 22, obj.spiel.spieler.taetigkeit, font_style)
			ws.write(row_num, 23, str(obj.spiel.spieler.wohnort), font_style)
			ws.write(row_num, 24, str(obj.spiel.spieler.wohnortLeben), font_style)
			ws.write(row_num, 25, obj.spiel.spieler.wohnortEltern, font_style)
			ws.write(row_num, 26, obj.spiel.spieler.erkannt, font_style)
			ws.write(row_num, 39, obj.spiel.spieler.anmerkungen, font_style)
		wb.save(response)
		return response
	else:
		if aSeite > 0:
			prev = aSeite - 1
		if aCount > (aSeite + 1) * maxPerPage:
			next = aSeite + 1
		# Antworten ... weiter
		aNr = aSeite * maxPerPage
		for aAntwort in aAntwortenM[aSeite * maxPerPage:aSeite * maxPerPage + maxPerPage]:
			aNr += 1
			aAuswertungen.append({'aNr': aNr, 'model': aAntwort})

		return render_to_response('evaluation/auswertungstart.html', RequestContext(request, {'aAuswertungen': aAuswertungen, 'aCount': aCount, 'prev': prev, 'next': next}))
