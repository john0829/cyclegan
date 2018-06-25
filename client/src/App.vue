<template>
  <div id="app">
    <button-r-outer ref="buttonRouter"></button-r-outer>
    <!-- <img src="./assets/logo.png"> -->
    <transition name="slide-fade">
      <router-view/>
    </transition>
  </div>
</template>

<script>
import ButtonROuter from '@/components/ButtonRouter'
export default {
  name: 'App',
  components:{
    ButtonROuter
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
