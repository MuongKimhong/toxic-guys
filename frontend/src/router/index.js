import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index';

import HomeView from '../views/HomeView.vue'
import SignIn from "../views/SignIn.vue";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: "/sign-in",
    name: "SignIn",
    component: SignIn,
    beforeEnter: (to, from, next) => {
      if (store.state.user.accessToken != null) next({ name: 'Home' });
      else next();
    },
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
