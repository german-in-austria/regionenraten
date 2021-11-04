"""Anzeige für Startseite."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Sum, Count

import os
import json

pOrte = [
	{'s': 'GAW', 'sf': 'GAW', 't': 'Gaweinstal', 'bl': 'Niederösterreich', 'dr': 'Ostmittelbairisch', 'cy': 420.4, 'cx': 2725.5},
	{'s': 'HÜT', 'sf': 'HUET', 't': 'Hüttschlag', 'bl': 'Salzburg', 'dr': 'Südmittelbairisch', 'cy': 1126.2, 'cx': 1503.1},
	{'s': 'NEC', 'sf': 'NEC', 't': 'Neckenmarkt', 'bl': 'Burgenland', 'dr': 'Südmittelbairisch', 'cy': 896.3, 'cx': 2714.1},
	{'s': 'NEU', 'sf': 'NEU', 't': 'Neumarkt an der Ybbs', 'bl': 'Niederösterreich', 'dr': 'Ostmittelbairisch', 'cy': 605, 'cx': 2168.7},
	{'s': 'RAG', 'sf': 'RAG', 't': 'Raggal', 'bl': 'Vorarlberg', 'dr': 'Alemannisch', 'cy': 1107.3, 'cx': 266.8},
	{'s': 'TAR', 'sf': 'TAR', 't': 'Tarrenz', 'bl': 'Tirol', 'dr': 'Bairisch-Alemannisch', 'cy': 1079.5, 'cx': 604.8},
	{'s': 'TAU', 'sf': 'TAU', 't': 'Taufkirchen an der Pram', 'bl': 'Oberösterreich', 'dr': 'Ostmittelbairisch', 'cy': 457.4, 'cx': 1614.2, 'top': True},
	{'s': 'TUX', 'sf': 'TUX', 't': 'Tux', 'bl': 'Tirol', 'dr': 'Südbairisch', 'cy': 1137.1, 'cx': 945.4},
	{'s': 'WEI', 'sf': 'WEI', 't': 'Weißbriach', 'bl': 'Kärnten', 'dr': 'Südbairisch', 'cy': 1387.8, 'cx': 1511.2},
	{'s': 'BRE', 'sf': 'BRE', 't': 'Bregenz', 'bl': 'Vorarlberg', 'dr': 'Alemannisch', 'cy': 950.4, 'cx': 233.4},
	{'s': 'INN', 'sf': 'INN', 't': 'Innsbruck', 'bl': 'Tirol', 'dr': 'Südbairisch', 'cy': 1077.1, 'cx': 833.2, 'top': True},
	{'s': 'LIE', 'sf': 'LIE', 't': 'Lienz', 'bl': 'Tirol', 'dr': 'Südbairisch', 'cy': 1312.1, 'cx': 1334.6},
	{'s': 'KLA', 'sf': 'KLA', 't': 'Klagenfurt', 'bl': 'Kärnten', 'dr': 'Südbairisch', 'cy': 1422.4, 'cx': 1896.1},
	{'s': 'SBG', 'sf': 'SBG', 't': 'Salzburg', 'bl': 'Salzburg', 'dr': 'Südmittelbairisch', 'cy': 789.8, 'cx': 1434.7},
	{'s': 'STY', 'sf': 'STY', 't': 'Steyrling', 'bl': 'Oberösterreich', 'dr': 'Ostmittelbairisch', 'cy': 787.3, 'cx': 1830.5},
	{'s': 'LIN', 'sf': 'LIN', 't': 'Linz', 'bl': 'Oberösterreich', 'dr': 'Ostmittelbairisch', 'cy': 515.5, 'cx': 1887.9},
	{'s': 'OWÖ', 'sf': 'OWOE', 't': 'Oberwölz', 'bl': 'Steiermark', 'dr': 'Südbairisch', 'cy': 1111.8, 'cx': 1885.4},
	{'s': 'PAS', 'sf': 'PAS', 't': 'Passail', 'bl': 'Steiermark', 'dr': 'Südmittelbairisch', 'cy': 1069.9, 'cx': 2334.6},
	{'s': 'GRA', 'sf': 'GRA', 't': 'Graz', 'bl': 'Steiermark', 'dr': 'Südmittelbairisch', 'cy': 1176.2, 'cx': 2305.9},
	{'s': 'EIS', 'sf': 'EIS', 't': 'Eisenstadt', 'bl': 'Burgenland', 'dr': 'Ostmittelbairisch', 'cy': 765.5, 'cx': 2700.1},
	{'s': 'ALL', 'sf': 'ALL', 't': 'Allentsteig', 'bl': 'Niederösterreich', 'dr': 'Ostmittelbairisch', 'cy': 300.6, 'cx': 2267},
	{'s': 'STP', 'sf': 'STP', 't': 'St.Pölten', 'bl': 'Niederösterreich', 'dr': 'Ostmittelbairisch', 'cy': 568.4, 'cx': 2374.5, 'top': True},
	{'s': 'WIE', 'sf': 'WIE', 't': 'Wien', 'bl': 'Wien', 'dr': 'Ostmittelbairisch', 'cy': 571.2, 'cx': 2645.5},
]


def start(request):
	"""Startseite."""
	return render_to_response(
		'vr/start.html',
		RequestContext(request, {'mediaUrl': settings.MEDIA_URL, 'gData': {'orte': pOrte}}),)


def data(request):
	"""Daten abfragen/setzen durch VUE."""
	import vr.models as dbmodels
	if 'set' in request.POST:
		# Speichere Spracheinstellung
		if request.POST.get('set') == 'playerDataSe':
			aData = json.loads(request.POST.get('data'))
			aSpieler = dbmodels.spieler.objects.get(uuid=request.POST.get('playerUuId'))  # Überprüfen ob Spiel mit Spieler existiert
			aSpieler.erkannt = aData['data']['erkannt'].strip()
			aSpieler.anmerkungen = aData['data']['anmerkungen'].strip()
			aSpieler.save()
			return httpOutput(json.dumps({'OK': True, 'playerUuId': str(aSpieler.uuid)}), mimetype='application/json; charset=utf-8')
		# Speichere Spielerdaten
		if request.POST.get('set') == 'playerData':
			aData = json.loads(request.POST.get('data'))
			aSpieler = dbmodels.spieler()
			aSpieler.geburtsjahr = int(aData['data']['geburtsjahr'])
			aSpieler.gesch = int(aData['data']['gesch'])
			aSpieler.taetigkeit = str(aData['data']['taetigkeit']['type']) + ' - ' + aData['data']['taetigkeit']['text'].strip()
			aSpieler.wohnort = str(aData['data']['wohnort']['ort']).strip() + ', ' + str(aData['data']['wohnort']['plz']).strip()
			wohnortLeben = ''
			for aOrt in aData['data']['wohnortLeben']:
				wohnortLeben += str(aOrt['ort']).strip() + ', ' + str(aOrt['plz']).strip() + ', ' + str(aOrt['von']).strip() + ' - ' + str(aOrt['bis']).strip() + '; '
			aSpieler.wohnortLeben = wohnortLeben
			wohnortEltern = ''
			for aOrt in aData['data']['wohnortEltern']:
				wohnortEltern += str(aOrt['ort']).strip() + ', ' + str(aOrt['plz']).strip() + '; '
			aSpieler.wohnortEltern = wohnortEltern
			aSpieler.dsgvo = aData['data']['dsgvo']
			aSpieler.save()
			return httpOutput(json.dumps({'OK': True, 'playerUuId': str(aSpieler.uuid)}), mimetype='application/json; charset=utf-8')
		# Speichere Spielrunde
		if request.POST.get('set') == 'gameRound' and 'playerUuId' in request.POST:
			aData = json.loads(request.POST.get('data'))  # {'selOrt': 'NEU', 'played': 1, 'beispielNr': 0, 'gId': 11, 'hochdeutsch': 3, 'orf': 3, 'pOrt' : '', 'aufgefallen,: '', 'aId': 12}
			aGame = dbmodels.spiel.objects.get(pk=aData['gId'], spieler__uuid=request.POST.get('playerUuId'))  # Überprüfen ob Spiel mit Spieler existiert
			aAntwort = dbmodels.antworten()
			aAntwort.spiel = aGame
			aAntwort.audiodatei = dbmodels.audiodatei.objects.get(pk=aData['aId'])
			aAntwort.beispiel = aData['beispielNr']
			aAntwort.wiedergaben = aData['played']
			aAntwort.gewOrt = aData['selOrt']
			if aData['nOeSel'] and len(aData['nOeSel']) > 1:
				aAntwort.gewOrt = aData['nOeSel']
				if aData['nOeTxt'].strip() and len(aData['nOeTxt'].strip()) > 1:
					aAntwort.gewOrt = aData['nOeTxt'].strip()
			aAntwort.hochdeutsch = aData['hochdeutsch']
			aAntwort.orf = aData['orf']
			aAntwort.pOrt = aData['pOrt']
			aAntwort.aufgefallen = aData['aufgefallen']
			sollOrt = None
			selOrt = None
			for d in pOrte:
				if d['bl'] == aAntwort.audiodatei.ort:
					sollOrt = d
			for d in pOrte:
				if d['bl'] == aAntwort.gewOrt:
					selOrt = d
			if sollOrt and selOrt:
				if selOrt['bl'] == sollOrt['bl']:
					aAntwort.correctBl = True
				if selOrt['dr'] == sollOrt['dr']:
					aAntwort.correctDr = True
			aAntwort.save()
			aAntwort.audiodatei.benutzt += 1
			aAntwort.audiodatei.save()
			return httpOutput(json.dumps({'OK': True, 'playerUuId': request.POST.get('playerUuId')}), mimetype='application/json; charset=utf-8')
	if 'get' in request.POST:
		# Auswertung
		if request.POST.get('get') == 'auswertungsData' and 'playerUuId' in request.POST:
			auswertung = {
				'playerUuId': request.POST.get('playerUuId')
			}
			if auswertung['playerUuId']:
				aSpieler = dbmodels.spieler.objects.get(uuid=auswertung['playerUuId'])  # Überprüfen ob UuId existiert
				auswertung['antworten'] = dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk).count()
				auswertung['antwortenRichtigBl'] = dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk, correctBl=True).count()
				auswertung['antwortenRichtigDr'] = dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk, correctDr=True).count()
				auswertung['antwortenDialekt'] = dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk).count()
				auswertung['antwortenDialektRichtigBl'] = dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk, correctBl=True).count()
				auswertung['antwortenDialektRichtigDr'] = dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk, correctDr=True).count()
				auswertung['antwortenStandard'] = dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk).count()
				auswertung['antwortenStandardRichtigBl'] = dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk, correctBl=True).count()
				auswertung['antwortenStandardRichtigDr'] = dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk, correctDr=True).count()
				auswertung['statistik'] = []
				for x in [1, 2, 3, 4, 5]:
					auswertung['statistik'].append({
						'Bl': dbmodels.spieler.objects.filter(richtigeKlasseBl=x).count(),
						'Dr': dbmodels.spieler.objects.filter(richtigeKlasseDr=x).count()
					})
				auswertung['runden'] = []
				for antwort in dbmodels.antworten.objects.filter(spiel__spieler_id=aSpieler.pk):
					auswertung['runden'].append({
						'str': str(antwort),
						'gewOrt': antwort.gewOrt,
						'pOrt': antwort.pOrt,
						'correctBl': antwort.correctBl,
						'correctDr': antwort.correctDr,
						'audiodatei': {
							'file': antwort.audiodatei.file,
							'ort': antwort.audiodatei.ort
						}
					})
				auswertung['richtigeKlasseBl'] = aSpieler.richtigeKlasseBl
				auswertung['richtigeKlasseDr'] = aSpieler.richtigeKlasseDr
			return httpOutput(json.dumps(auswertung), mimetype='application/json; charset=utf-8')
		# Spiel Daten
		if request.POST.get('get') == 'gameData' and 'playerUuId' in request.POST:
			game = {
				'playerUuId': request.POST.get('playerUuId')
			}
			if game['playerUuId']:
				aSpiel = dbmodels.spiel()
				aSpiel.spieler = dbmodels.spieler.objects.get(uuid=game['playerUuId'])  # Überprüfen ob UuId existiert
				aSpiel.save()
				game['gId'] = aSpiel.pk
				from random import shuffle
				aFiles = []
				for aFile in dbmodels.audiodatei.objects.all():
					aFiles.append({'pk': aFile.pk, 'file': aFile.file, 'ort': aFile.ort, 'benutzt': aFile.benutzt})
				game['files'] = aFiles
				shuffle(game['files'])
				return httpOutput(json.dumps(game), mimetype='application/json; charset=utf-8')
	return httpOutput(json.dumps({'error': 'unknown request'}), mimetype='application/json; charset=utf-8')


def updateaudio(request):
	"""Audiodateien in Datenbank eintragen."""
	import vr.models as dbmodels
	if not request.user.is_authenticated():
		return httpOutput('Erst einloggen!')
	files = [f for f in os.listdir(settings.MEDIA_DIR) if os.path.isfile(os.path.join(settings.MEDIA_DIR, f))]
	aLen = 0
	aUpdate = 0
	output = ''
	for file in files:
		if file.split(".")[-1] == "ogg":
			uOrt = False
			try:
				dbmodels.audiodatei.objects.get(file=file)
				output += 'exists\n'
			except dbmodels.audiodatei.DoesNotExist:
				aUpdate += 1
				nAudiodatei = dbmodels.audiodatei()
				nAudiodatei.file = file
				nAudiodatei.benutzt = 0
				nAudiodatei.save()
				output += 'added\n'
	return httpOutput('Updated ... ' + str(aUpdate) + '/' + str(aLen) + '/' + str(len(files)) + '\n' + '-----' + '\n' + output)


def httpOutput(aoutput, mimetype='text/plain; charset=utf-8'):
	"""Einfache http Ausgabe."""
	txtausgabe = HttpResponse(aoutput)
	txtausgabe['Content-Type'] = mimetype
	return txtausgabe
