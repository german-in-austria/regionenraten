<template>
	<div class="form-group mb-0 p-relative">
		<label :for="'iWohnort' + _uid">{{ label }}</label>
		<template v-if="multi">
			<div class="form-row" v-for="(aValue, aKey) in value" :key="aKey">
				<div :class="'form-group col-sm-8 col-md-' + (zeitraum ? '6' : '8')"><input v-model="aValue.ort" @change="changed" @keyup="changed" type="text" :class="'form-control ' + (inputClass || '')" :id="'iWohnort' + _uid" placeholder="Wohnort"></div>
				<div :class="'form-group col-sm-4 col-md-' + (zeitraum ? '2' : '4')"><input v-model="aValue.plz" @change="changed" @keyup="changed" type="number" min="0" :class="'form-control ' + inputClass" placeholder="Postleitzahl"></div>
				<div class="form-group col-sm-6 col-md-2"><input v-model="aValue.von" @change="changed" type="text" :class="'form-control ' + inputClass" placeholder="Dort gelebt von" v-if="zeitraum"></div>
				<div class="form-group col-sm-6 col-md-2"><input v-model="aValue.bis" @change="changed" type="text" :class="'form-control ' + inputClass" placeholder="Dort gelebt bis" v-if="zeitraum"></div>
			</div>
			<div class="invalid-tooltip" style="display: block; top: calc( 100% - 1rem ); left: 5px;" v-if="error && error.error && error.msg && error.changed">{{ error.msg }}</div>
			<button @click="addWohnort()" type="button" class="btn btn-primary mb-3" v-if="!fix">Weiteren Ort hinzufügen</button>
		</template>
		<div class="form-row" v-else>
			<div class="form-group col-sm-8 col-md-8"><input v-model="value.ort" type="text" :class="'form-control ' + (inputClass || '')" :id="'iWohnort' + _uid" placeholder="Wohnort"></div>
			<div class="form-group col-sm-4 col-md-4"><input v-model="value.plz" type="number" min="0" :class="'form-control ' + inputClass" placeholder="Postleitzahl"></div>
			<div class="invalid-tooltip" style="display: block; top: calc( 100% - 1rem ); left: 5px;" v-if="error && error.error && error.msg && error.changed">{{ error.msg }}</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'Wohnort',
	props: ['label', 'value', 'inputClass', 'error', 'multi', 'zeitraum', 'fix'],
	data () {
		return {
		}
	},
	mounted () {
		if (this.multi) {
			if (this.value.length < 1) {
				this.addWohnort()
			}
		}
	},
	methods: {
		changed () {
			this.$emit('changed')
		},
		addWohnort () {
			let addData = {
				ort: '',
				plz: ''
			}
			if (this.zeitraum) {
				addData.von = ''
				addData.bis = ''
			}
			this.value.push(addData)
		}
	}
}
</script>

<style scoped>
	.p-relative {
		position: relative;
	}
</style>
