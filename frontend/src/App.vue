<template>

  <div>
    <p>Hello {{ name }}</p>
    <HelloWorld/>
    <div v-if="fruits">
      <p v-for="fruit in fruits" :key="fruit">{{ fruit }}</p>
    </div>
  </div>
 
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue"

export default {
  name: 'App',

  data(){
    return {
    name : "Ramya",
    fruits : null
    }
    
  },
  components:{
    HelloWorld
  },
  mounted(){
    const l = ["apple, banana"]
    this.fruits = l
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>