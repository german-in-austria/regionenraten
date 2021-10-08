from django.db import models
import uuid
import math
from vr.views import pOrte


class audiodatei(models.Model):
	added				= models.DateTimeField(auto_now_add=True																, verbose_name="Hinzugefügt")
	file				= models.CharField(max_length=255	, blank=True, null=True								, verbose_name="Dateiname")
	ort					= models.CharField(max_length=255	, blank=True, null=True								, verbose_name="Ort")
	benutzt			= models.IntegerField(				  blank=True, null=True										, verbose_name="Benutzt")

	def __str__(self):
		return '{} - {} ({})'.format(self.ort, self.file, self.added)

	class Meta:
		verbose_name = "Audiodatei"
		verbose_name_plural = "Audiodateien"
		ordering = ('ort', 'file', )


class antworten(models.Model):
	spiel				= models.ForeignKey('spiel'			, on_delete=models.CASCADE							, verbose_name="Spiel")
	beispiel		= models.IntegerField(				  blank=True, null=True										, verbose_name="Beispiel")
	zeit				= models.DateTimeField(auto_now_add=True																, verbose_name="Zeit")
	audiodatei	= models.ForeignKey('audiodatei'	, on_delete=models.CASCADE						, verbose_name="Audiodatei")
	wiedergaben	= models.IntegerField(				  blank=True, null=True										, verbose_name="Wiedergaben")
	gewOrt			= models.CharField(max_length=1024	, blank=True, null=True								, verbose_name="gewählter Ort")
	hochdeutsch = models.IntegerField(				  blank=True, null=True										, verbose_name="Hochdeutsch (1-7)")
	orf					= models.IntegerField(				  blank=True, null=True										, verbose_name="ORF (1-7)")
	pOrt				= models.CharField(max_length=1024	, blank=True, null=True							, verbose_name="präzisere Herkunft")
	aufgefallen	= models.CharField(max_length=1024	, blank=True, null=True							, verbose_name="aufgefallen")
	correctBl		= models.BooleanField(default=False																			, verbose_name="Richtiges Bundesland")
	correctDr		= models.BooleanField(default=False																			, verbose_name="Richtiger Dialektraum")

	def save(self, *args, **kwargs):
		try:
			aSpieler = self.spiel.spieler
			aAntw = antworten.objects.filter(spiel__spieler_id=aSpieler.pk).count()
			aRichtigeKlasseBl = None
			if aAntw > 0:
				aRichtigeKlasseBl = math.floor(4.99 / aAntw * antworten.objects.filter(spiel__spieler_id=aSpieler.pk, correctBl=True).count()) + 1
			aSpieler.richtigeKlasseBl = aRichtigeKlasseBl
			aRichtigeKlasseDr = None
			if aAntw > 0:
				aRichtigeKlasseDr = math.floor(4.99 / aAntw * antworten.objects.filter(spiel__spieler_id=aSpieler.pk, correctDr=True).count()) + 1
			aSpieler.richtigeKlasseDr = aRichtigeKlasseDr
			aSpieler.save()
		except Exception as e:
			print(e)
		super(antworten, self).save(*args, **kwargs)

	def __str__(self):
		return '{} [{}] [{}] {} {} ({}) - {}'.format(self.beispiel, 'X' if self.correctBl else ' ', 'X' if self.correctDr else ' ', self.hochdeutsch, self.orf, self.zeit, self.audiodatei)

	class Meta:
		verbose_name = "Antwort"
		verbose_name_plural = "Antworten"
		ordering = ('zeit', 'beispiel', )


class spiel(models.Model):
	spieler			= models.ForeignKey('spieler'		, on_delete=models.CASCADE							, verbose_name="Spieler")
	zeit			= models.DateTimeField(auto_now_add=True																	, verbose_name="Zeit")

	def __str__(self):
		return '{} ({}) - {}'.format(self.pk, self.zeit, self.spieler)

	class Meta:
		verbose_name = "Spiel"
		verbose_name_plural = "Spiele"
		ordering = ('spieler', 'zeit', )


class spieler(models.Model):
	zeit			= models.DateTimeField(auto_now_add=True																	, verbose_name="Zeit")
	uuid			= models.UUIDField(default=uuid.uuid4, editable=False, unique=True				, verbose_name="uuid")
	# Fragebogen mit Orten usw.
	geburtsjahr		= models.IntegerField(				  blank=True, null=True									, verbose_name="Geburtsjahr")
	gesch		= models.IntegerField(				  blank=True, null=True												, verbose_name="Geschlecht")
	taetigkeit = models.CharField(max_length=1024	, blank=True, null=True								, verbose_name="Tätigkeit")
	wohnort			= models.CharField(max_length=1024	, blank=True, null=True								, verbose_name="Wohnort")
	wohnortLeben	= models.CharField(max_length=1024	, blank=True, null=True							, verbose_name="Wohnort Leben")
	wohnortEltern	= models.CharField(max_length=1024	, blank=True, null=True							, verbose_name="Wohnort Eltern")
	dsgvo			= models.BooleanField(default=False																				, verbose_name="DSGVO")
	# Nach dem Spiel
	erkannt	= models.CharField(max_length=1024	, blank=True, null=True							, verbose_name="Erkannt")
	anmerkungen	= models.CharField(max_length=1024	, blank=True, null=True							, verbose_name="Anmerkungen")
	# Cach
	richtigeKlasseBl = models.IntegerField(				  blank=True, null=True								, verbose_name="Richtig Bundesland (1 = 0%-20%, 2 = 20%-40%, ...)")
	richtigeKlasseDr = models.IntegerField(				  blank=True, null=True								, verbose_name="Richtig Dialektregion (1 = 0%-20%, 2 = 20%-40%, ...)")

	def __str__(self):
		return '{} ({} - {})'.format(self.pk, self.zeit, self.uuid)

	class Meta:
		verbose_name = "Spieler"
		verbose_name_plural = "Spieler"
		ordering = ('zeit', )
