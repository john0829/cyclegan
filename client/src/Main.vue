<template>
  <div id="main">
    <real-to-anime ref="realToAnime"></real-to-anime>
    <anime-to-real ref="animeToReal"></anime-to-real>
    <transition name="slide-fade">
      <router-view></router-view>
    </transition>
  </div>
</template>

<script>
import RealToAnime from '@/components/RealToAnime'
import AnimeToReal from '@/components/AnimeToReal'
export default {
  name: 'Main',
  components:{
    RealToAnime,
    AnimeToReal,
  }
}
</script>

<style>
#main {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}


.slide-fade-enter-active {
  transition: all .3s ease;
}

.slide-fade-leave-active {
  transition: all .3s cubic-bezier(1.0,0.5,0.8,1.0);
}

.slide-fade-enter-active ,.slide-fade-leave-active{
  transform: translateX(500px);
  opacity: 0;
}
</style>
