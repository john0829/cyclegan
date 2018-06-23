<template>
  <div class="hello container">
    <div class="row">
      <router-link :to="{path:'/live'}" class="btn btn-info col-2" tag="button">live</router-link>
      <div class="col-1"></div>
      <router-link :to="{path:'/'}" class="btn btn-info col-2" tag="button">file</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      imageData:"./static/sampleReal.jpg",
      modifiedImage:"./static/sampleChangeAnime.jpg"
    }
  },
  methods:{

  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
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

img{
  width:300px;
  height:300px;
}

div{
  margin-bottom: 50px;
}
</style>
