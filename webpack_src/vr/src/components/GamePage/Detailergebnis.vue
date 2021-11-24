<template>
	<div class="text-center">
		<h1>Detailergebnis</h1>
		<br>
		<div v-if="auswertungsData.auswertung && auswertungsData.auswertung.ready && auswertungsData.auswertung.data">
			<p>
				<!-- <p>Sie haben <b>{{ auswertungsData.auswertung.data.antwortenRichtigDr }}</b> von <b>{{ auswertungsData.auswertung.data.antworten }}</b> Sprecherinnen und Sprechern richtig ihren <b>Dialektregionen</b> zugeordnet.<br> -->
				Sie haben <b>{{ auswertungsData.auswertung.data.antwortenRichtigBl }}</b> von <b>{{ auswertungsData.auswertung.data.antworten }}</b> Sprecherinnen und Sprechern richtig ihren <b>Bundesländern</b> zugeordnet.<br>
			</p>
			<p>Im Vergleich mit den anderen Spielenden liegen Sie hier:</p>
			<div>
				<svg viewBox="-20 -5 425 210" class="border">
					<template v-for="y in 11">
						<g :transform="'translate(0 ' + ((y - 1) * 18 + 0.5) + ')'" :key="y">
							<line x1="0" x2="400" :y1="0" :y2="0" style="stroke: #eee; stroke-width: 0.5;"/>
							<text x="-2" y="2" text-anchor="end" fill="#888" style="font-size: 7px">{{ parseInt(100 / statistikMax.maxSum * statistikMax.max / 10 * (11 - y)) }} %</text>
						</g>
					</template>
					<g :transform="'translate(' + (40 + x * 80) + ' 180)'" v-for="(y, x) in auswertungsData.auswertung.data.statistik" :key="x + 'x' + y">
						<rect x="-10" width="20" :y="0.5 + -180 / statistikMax.Bl * y.Bl" :height="180 / statistikMax.Bl * y.Bl" :class="'chart chartbl' + ((auswertungsData.auswertung.data.richtigeKlasseBl === x + 1) ? ' active' : '')"/>
						<!-- <rect x="-13" width="10" :y="0.5 + -180 / statistikMax.Dr * y.Dr" :height="180 / statistikMax.Dr * y.Dr" :class="'chart chartdr' + ((auswertungsData.auswertung.data.richtigeKlasseDr === x + 1) ? ' active' : '')"/> -->
						<text x="0" y="15" text-anchor="middle" style="font-size: 8px">{{ ['0%-20% richtig', '20%-40% richtig', '40%-60% richtig', '60%-80% richtig', '80%-100% richtig'][x] }}</text>
					</g>
				</svg>
			</div>
			<br>
			<!-- <p><span class="colbox colboxdr">&nbsp;</span> = Dialektregion, <span class="colbox colboxbl">&nbsp;</span> = Bundesland<br></p> -->
			<br>
			<p><b>Danke, dass Sie mitgespielt haben!</b></p>
		</div>
		<br>
		<button @click="$emit('next')" type="button" class="btn btn-primary" v-if="devMode">Restart</button>
		<a href="https://www.dioe.at/ergebnisse" class="btn btn-primary">Ende</a>
		<br><br>
		<div class="loading" v-if="!(auswertungsData.auswertung && auswertungsData.auswertung.ready)">Lade ... <button @click="reload()" v-if="devMode" style="font-size:20px;">Reload</button></div>
		<button @click="reload()" v-if="devMode">Reload</button>
		<div class="mt-4" v-if="auswertungsData.auswertung && auswertungsData.auswertung.ready && auswertungsData.auswertung.data">
			<table class="table">
				<thead>
					<tr>
						<th scope="col">#</th>
						<th scope="col">Ihr Tipp</th>
						<th scope="col">korrekte Antwort</th>
						<th scope="col">Sprachbeispiel</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(runde, dg) in auswertungsData.auswertung.data.runden" :key="dg" :class="{'ant-list-tr': true, 'correct-bl': runde.correctBl, 'correct-dr': runde.correctDr}">
						<th scope="row">{{ dg + 1 }}</th>
						<td>{{ runde.gewOrt + (runde.pOrt ? ', ' + runde.pOrt : '') }}</td>
						<td>{{ runde.audiodatei.ort }}</td>
						<td>
							<audio controls preload="none" class="audioPlayer" controlsList="nodownload noplaybackrate">
								<source :src="mediaUrl + runde.audiodatei.file" type="audio/ogg">
							</audio>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>

<script>
	/* global mediaUrl */
	export default {
		name: 'Detailergebnis',
		data () {
			return {
				devMode: (process.env.NODE_ENV === 'development'),
				auswertungsData: {},
				mediaUrl: mediaUrl,
			}
		},
		computed: {
			statistikMax () {
				let aSumBl = 0
				let aSumDr = 0
				let aMaxBl = 0
				let aMaxDr = 0
				if (this.auswertungsData && this.auswertungsData.auswertung && this.auswertungsData.auswertung.data) {
					this.auswertungsData.auswertung.data.statistik.forEach(function (x) {
						aSumBl += x['Bl']
						aSumDr += x['Dr']
						if (x['Bl'] > aMaxBl) {
							aMaxBl = x['Bl']
						}
						if (x['Dr'] > aMaxDr) {
							aMaxDr = x['Dr']
						}
					}, this)
				}
				return {'Bl': aMaxBl, 'Dr': aMaxDr, 'max': (aMaxBl > aMaxDr ? aMaxBl : aMaxDr), 'sBl': aSumBl, 'sDr': aSumDr, 'maxSum': (aSumBl > aSumDr ? aSumBl : aSumDr)}
			},
		},
		watch: {
			'auswertungsData' (nVal) {
				if (nVal) {
					if (this.devMode) {
						console.log(this.auswertungsData, this.statistikMax)
					}
				}
			},
		},
		methods: {
			reload () {
				this.loading = true
				this.auswertungsData = {}
				this.$emit('getAuswertungsData', this.auswertungsData)
			},
		},
		mounted () {
			this.reload()
		},
	}
</script>

<style scoped>
	.loading {
		position: fixed;
		left: 0;
		top: 0;
		right: 0;
		bottom: 0;
		padding-top: 40vh;
		text-align: center;
		color: #fff;
		background: #000;
		background: rgba(0,0,0,0.5);
		font-size: 60px;
	}
	rect.chartdr {
		fill: #007bff;
	}
	rect.chartbl {
		fill: #28a745;
	}
	rect.chart.active {
		stroke-width: 1;
		stroke: #dc3545;
	}
	.colbox {
		display: inline-block;
		width: 26px;
	}
	.colboxdr {
		background: #007bff;
	}
	.colboxbl {
		background: #28a745;
	}
	.audioPlayer {
		height: 30px;
	}
	.ant-list-tr {
		background: #ffeeee;
	}
	/* .correct-dr {
		background: #e9f4ff;
	} */
	.correct-bl {
		background: #eefff2;
	}
</style>
