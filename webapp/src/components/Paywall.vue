<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
			Hello Raiden!
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class PaywalledContent extends Vue {
  @Prop() private msg!: string;

	async mounted(){
		this.$http.get('http://localhost:5000');
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
