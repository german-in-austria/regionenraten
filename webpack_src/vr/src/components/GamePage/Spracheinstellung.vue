<template>
	<div>
		<h1 class="text-center">2 letzte Fragen</h1>
		<br>
		<div class="alert alert-primary" role="alert">
			Bevor es zu den Ergebnissen geht, haben wir noch 2 letzte Fragen an Sie:
		</div>

		<div class="form-group" style="position: relative;">
			<label for="inputErkannt">Haben Sie eine*n der Sprecher*innen womöglich erkannt? (Name)</label>
			<input v-model="daten.erkannt" type="text" class="form-control" id="inputErkannt" placeholder="">
		</div>

		<div class="form-group" style="position: relative;">
			<label for="inputAnmerkungen">Haben Sie noch Anmerkungen? </label>
			<input v-model="daten.anmerkungen" type="text" class="form-control" id="inputAnmerkungen" placeholder="">
		</div>

		<div class="alert alert-danger mt-3" role="alert" v-if="errors > 0">
			<h5>Formular enthält Fehler:</h5>
			<ul class="mb-0">
				<template v-for="(aError, aKey) in error">
					<li v-if="aError.error" :key="aKey">{{ aError.msg }}</li>
				</template>
			</ul>
		</div>

		<button @click="nextStep()" type="button" class="btn btn-primary w-100" :disabled="errors > 0">Weiter zu den Detailergebnissen</button>

	</div>
</template>

<script>
	export default {
		name: 'Spracheinstellung',
		data () {
			return {
				errors: 0,
				daten: {
					erkannt: '',
					anmerkungen: ''
				}
			}
		},
		methods: {
			nextStep () {
				if (this.errors === 0) {
					this.$emit('savedataSe', JSON.parse(JSON.stringify(this.daten)))
					this.$nextTick(() => { this.$emit('next') })
				} else {
					alert('Das Formular enthält noch Fehler!')
				}
			},
		},
		mounted () {
		},
	}
</script>

<style scoped>
</style>
