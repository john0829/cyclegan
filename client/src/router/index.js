import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/Main'
import Live from '@/Live'

Vue.use(Router)

export default new Router({
  base: __dirname,
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/live',
      name: 'Live',
      component: Live
    },
  ]
})
