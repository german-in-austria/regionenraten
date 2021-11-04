<template>
	<div>
		<div class="alert alert-primary" role="alert">
			Bitte geben Sie folgende Informationen zu Ihrer Person an, die für die spätere Auswertung Ihrer Antworten erforderlich sind. Selbstverständlich werden alle Angaben anonym behandelt. <i>(* Pflichtfelder)</i>
		</div>

		<div class="form-group p-relative">
			<label>Welchem Geschlecht fühlen Sie sich zugehörig? *</label>
			<div :class="'form-control' + ((error.gesch.error) ? ' is-invalid' : ' is-valid')" style="height: auto;">
				<div class="form-check form-check-inline" v-for="(aCheck, aKey) in [{val: 1, title: 'männlich', id: 'srman'}, {val: 2, title: 'weiblich', id: 'srwoman'}, {val: 3, title: 'divers', id: 'srsonst'}]" :key="aKey">
					<input v-model="daten.gesch" class="form-check-input" type="radio" name="inputgesch" :id="aCheck.id" :value="aCheck.val">
					<label class="form-check-label" :for="aCheck.id">{{ aCheck.title }}</label>
				</div>
			</div>
		</div>
		<div class="form-group p-relative">
			<label for="inputGeburtsjahr">Wie lautet ihr Geburtsjahr? *</label>
			<input v-model="daten.geburtsjahr" type="number" min="1890" max="2020" :class="'form-control' + ((error.geburtsjahr.error) ? ' is-invalid' : ' is-valid')" id="inputGeburtsjahr" placeholder="Geburtsjahr">
			<div class="invalid-tooltip" v-if="error.geburtsjahr.changed">{{ error.geburtsjahr.msg }}</div>
		</div>
		<div class="form-group p-relative">
			<label>Welche Tätigkeit üben Sie aus? *</label>
			<div :class="'form-control' + ((error.taetigkeit.error) ? ' is-invalid' : ' is-valid')" style="height: auto;">
				<div class="form-check form-check-inline" v-for="(aCheck, aKey) in [{val: 'studentin', title: 'Student*in', id: 'studentin'}, {val: 'andere', title: 'andere Tätigkeit', id: 'andere'}]" :key="aKey">
					<input v-model="daten.taetigkeit.type" class="form-check-input" type="radio" name="inputTaetigkeit" :id="aCheck.id" :value="aCheck.val">
					<label class="form-check-label" :for="aCheck.id">{{ aCheck.title }}</label>
				</div>
			</div>
		</div>
		<div class="form-group p-relative" v-if="daten.taetigkeit.type">
			<label for="inputTaetigkeitText">{{ daten.taetigkeit.type === 'studentin' ? 'Fach/Studienrichtung' : 'Welche Tätigkeit üben Sie aus?' }} *</label>
			<input v-model="daten.taetigkeit.text" type="text" :class="'form-control' + ((error.taetigkeit.error) ? ' is-invalid' : ' is-valid')" id="inputTaetigkeitText">
			<div class="invalid-tooltip" v-if="error.taetigkeit.changed">{{ error.taetigkeit.msg }}</div>
		</div>
		<Wohnort v-model="daten.wohnort" :error="error.wohnort" :inputClass="((error.wohnort.error) ? ' is-invalid' : ' is-valid')" label="Wie lautet ihr aktueller Wohnort? *"/>
		<Wohnort v-model="daten.wohnortLeben" :multi="true" :zeitraum="true" @changed="debouncedCheckErrors"  label="An welchen anderen Orten haben Sie gelebt?"/>
		<Wohnort v-model="daten.wohnortEltern" @changed="debouncedCheckErrors" :multi="true" :fix="true" label="Wo sind Ihre Eltern aufgewachsen?"/>

		<div class="alert alert-primary mt-3" role="alert">
			<h4 class="mb-3">Der SFB „Deutsch in Österreich“ behandelt Ihre Daten vertraulich und ausschließlich für wissenschaftliche Zwecke.</h4>
			<div class="form-group p-relative form-check bg-white p-3 px-5 mb-2 rounded">
				<input v-model="daten.dsgvo" type="checkbox" :class="'form-check-input' + ((error.dsgvo.error) ? ' is-invalid' : ' is-valid')" id="dsgvoCheck">
				<label class="form-check-label" for="dsgvoCheck">Ich erkläre mich damit einverstanden, dass meine personenbezogenen Daten - wie in der <a href="https://www.dioe.at/datenschutz/" target="_blank">Datenschutzerklärung</a> beschrieben - vom SFB „Deutsch in Österreich: Variation – Kontakt – Perzeption“ wissenschaftlich ausgewertet werden und im Zuge dessen innerhalb des SFBs verwendet werden. Diese Einwilligung kann ich jederzeit widerrufen.</label>
				<div class="invalid-tooltip" v-if="error.dsgvo.changed">{{ error.dsgvo.msg }}</div>
			</div>
		</div>

		<div class="alert alert-danger mt-3" role="alert" v-if="errors > 0">
			<h5>Formular enthält Fehler:</h5>
			<ul class="mb-0">
				<template v-for="(aError, aKey) in error">
					<li v-if="aError.error" :key="aKey">{{ aError.msg }}</li>
				</template>
			</ul>
		</div>

		<button @click="nextStep()" type="button" class="btn btn-primary w-100" :disabled="errors > 0">Los geht’s</button>

		<div class="loading" v-if="saving">Speichere ...</div>

	</div>
</template>

<script>
import RadioFromTo from './formular/RadioFromTo'
import Wohnort from './formular/Wohnort'
import _ from 'lodash'

export default {
	name: 'DataPage',
	data () {
		return {
			saving: false,
			errors: 0,
			daten: {
				geburtsjahr: null,
				gesch: 0,
				taetigkeit: {
					type: 0,
					text: ''
				},
				wohnort: {
					ort: '',
					plz: ''
				},
				wohnortLeben: [],
				wohnortEltern: [
					{
						ort: '',
						plz: ''
					},
					{
						ort: '',
						plz: ''
					}
				],
				dsgvo: false
			},
			error: {
				geburtsjahr: {
					check: function (val) { return (val >= 1890 && val <= 2021) },
					msg: 'Geburtsjahr muss nach 1890 liegen und vierstellig angegeben werden!'
				},
				gesch: {
					check: function (val) { return (val > 0 && val < 4) },
					msg: 'Bitte geben Sie Ihr Geschlecht an!'
				},
				taetigkeit: {
					check: function (val) { return val.type && val.text },
					msg: 'Bitte geben Sie Ihre Tätigkeit an!'
				},
				wohnort: {
					check: function (val) { return val.ort && val.plz },
					msg: 'Bitte geben Sie Ihren Wohnort mit Postleitzahl an!'
				},
				// wohnortEltern: {
				// 	check: function (val) { return val[0].ort && val[0].plz },
				// 	msg: 'Bitte geben Sie den Wohnort Ihrer Eltern an!'
				// },
				dsgvo: {
					check: function (val) { return val },
					msg: 'Bitte stimmen Sie der Verarbeitung Ihrer personenbezogenen Daten zu!'
				},
			}
		}
	},
	watch: {
	},
	methods: {
		checkErrors () {
			this.errors = 0
			Object.keys(this.daten).forEach(function (aKey) {
				this.checkError(aKey)
				if (this.error[aKey].error) {
					this.errors += 1
				}
			}, this)
		},
		checkError (aKey, uVal = undefined) {
			let cVal = uVal
			if (cVal === undefined) {
				cVal = this.daten[aKey]
			}
			if (!this.error[aKey]) {
				this.error[aKey] = {}
			}
			this.$set(this.error[aKey], 'error', false)
			if (this.error[aKey].check) {
				if (!this.error[aKey].check(cVal, this.daten)) {
					this.$set(this.error[aKey], 'error', true)
				}
			}
			this.$set(this.error[aKey], 'empty', true)
			if (cVal) {
				if (typeof cVal === 'object') {
					Object.keys(cVal).some(function (aProp) {
						if (cVal[aProp]) {
							this.$set(this.error[aKey], 'empty', false)
							return true
						}
					}, this)
				} else {
					this.$set(this.error[aKey], 'empty', false)
				}
			}
		},
		debouncedCheckErrors: _.debounce(function () {
			this.checkErrors()
		}, 250),
		initCheckErrors () {
			this.checkErrors()
			Object.keys(this.error).forEach(function (aKey) {
				if (this.daten[aKey] && typeof this.daten[aKey] === 'object') {
					Object.keys(this.daten[aKey]).forEach(function (aProp) {
						if (this.daten[aKey][aProp] || this.daten[aKey][aProp] === 0 || this.daten[aKey][aProp] === '') {
							this.$watch('daten.' + aKey + '.' + aProp, function (nVal) { this.$nextTick(() => { this.$set(this.error[aKey], 'changed', true); this.debouncedCheckErrors() }) })
						}
					}, this)
				} else {
					this.$watch('daten.' + aKey, function (nVal) { this.$nextTick(() => { this.$set(this.error[aKey], 'changed', true); this.debouncedCheckErrors() }) })
				}
			}, this)
		},
		nextStep () {
			if (this.errors === 0) {
				this.$emit('savedata', JSON.parse(JSON.stringify(this.daten)))
				this.saving = true
			} else {
				alert('Das Formular enthält noch Fehler!')
			}
		},
	},
	mounted () {
		this.initCheckErrors()
	},
	components: {
		RadioFromTo,
		Wohnort,
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
	.p-relative {
		position: relative;
	}
</style>
