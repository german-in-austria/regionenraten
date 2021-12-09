<template>
	<div class="text-center">
		<h1>Regionen raten – So klingt Österreich</h1>
		<img src="/static/main/bilder/Regionen_raten_Titelgrafik4.png" class="img-fluid title-img my-3 my-lg-5">
		<p>„Glauben Sie, man kann beim Vorlesen verstecken, woher man stammt? In diesem Quiz können Sie es herausfinden!“</p>
		<p>Testen Sie ihr Sprachgefühl, messen Sie sich mit anderen Teilnehmenden und leisten Sie damit gleichzeitig einen wichtigen Beitrag zu unserer Forschung.</p>
		<p>Wir wünschen Ihnen viel Spaß und bedanken uns herzlich für Ihre Teilnahme!</p>
		<br>
		<button @click="$emit('start')" type="button" class="btn btn-primary">Starten ...</button>
	</div>
</template>

<script>
	export default {
		name: 'StartPage',
		data () {
			return {
			}
		},
	}
</script>

<style scoped>
	.title-img {
		width: auto;
		max-height: 40vh;
	}
</style>
