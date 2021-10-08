<template>
	<div class="text-center">
		<h1>Detailergebnis</h1>
		<br>
		<div v-if="auswertungsData.auswertung && auswertungsData.auswertung.ready && auswertungsData.auswertung.data">
			<p>Sie haben <b>{{ auswertungsData.auswertung.data.antwortenRichtigDr }}</b> von <b>{{ auswertungsData.auswertung.data.antworten }}</b> Sprecherinnen und Sprechern richtig ihren <b>Dialektregionen</b> zugeordnet.<br>
			Sie haben <b>{{ auswertungsData.auswertung.data.antwortenRichtigBl }}</b> von <b>{{ auswertungsData.auswertung.data.antworten }}</b> Sprecherinnen und Sprechern richtig ihren <b>Bundesländern</b> zugeordnet.<br>
			<p>Im Vergleich mit anderen Spielenden liegen sie damit hier:</p>
			<div>
				<svg viewBox="-5 -5 410 210" class="border">
					<line x1="0" x2="400" :y1="(y - 1) * 18 + 0.5" :y2="(y - 1) * 18 + 0.5" style="stroke: #eee; stroke-width: 0.5;" v-for="y in 11" :key="y"/>
					<g :transform="'translate(' + (40 + x * 80) + ' 180)'" v-for="(y, x) in auswertungsData.auswertung.data.statistik" :key="x + 'x' + y">
						<rect x="2" width="10" :y="0.5 + -180 / statistikMax.Bl * y.Bl" :height="180 / statistikMax.Bl * y.Bl" :class="'chart chartbl' + ((auswertungsData.auswertung.data.richtigeKlasseBl === x + 1) ? ' active' : '')"/>
						<rect x="-13" width="10" :y="0.5 + -180 / statistikMax.Dr * y.Dr" :height="180 / statistikMax.Dr * y.Dr" :class="'chart chartdr' + ((auswertungsData.auswertung.data.richtigeKlasseDr === x + 1) ? ' active' : '')"/>
						<text x="0" y="15" text-anchor="middle" style="font-size: 8px">{{ ['0%-20% richtig', '20%-40% richtig', '40%-60% richtig', '60%-80% richtig', '80%-100% richtig'][x] }}</text>
					</g>
				</svg>
			</div>
			<br>
			<p><span class="colbox colboxdr">&nbsp;</span> = Dialektregion, <span class="colbox colboxbl">&nbsp;</span> = Bundesland<br></p>
			<br>
			<p><b>Danke, dass Sie mitgespielt haben!</b></p>
		</div>
		<br>
		<button @click="$emit('next')" type="button" class="btn btn-primary">Ende</button><br><br>
		<div class="loading" v-if="!(auswertungsData.auswertung && auswertungsData.auswertung.ready)">Lade ... <button @click="reload()" v-if="devMode" style="font-size:20px;">Reload</button></div>
		<button @click="reload()" v-if="devMode">Reload</button>
	</div>
</template>

<script>
	export default {
		name: 'Detailergebnis',
		data () {
			return {
				devMode: (process.env.NODE_ENV === 'development'),
				auswertungsData: {},
			}
		},
		computed: {
			statistikMax () {
				let aMax = 0
				let aMaxBl = 0
				let aMaxDr = 0
				this.auswertungsData.auswertung.data.statistik.forEach(function (x) {
					if (x['Ho'] > aMax) {
						aMax = x['Ho']
					}
					if (x['Bl'] > aMaxBl) {
						aMaxBl = x['Bl']
					}
					if (x['Dr'] > aMaxDr) {
						aMaxDr = x['Dr']
					}
				}, this)
				return {'Ho': aMax, 'Bl': aMaxBl, 'Dr': aMaxDr}
			},
		},
		watch: {
			'auswertungsData' (nVal) {
				if (nVal) {
					if (this.devMode) {
						console.log(this.auswertungsData)
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
</style>
