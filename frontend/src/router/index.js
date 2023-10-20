import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index';

import SignIn from "../views/SignIn.vue";
import SignUp from "../views/SignUp.vue";

import Home from '../views/Home.vue';
import Profile from "../views/Profile.vue";
import Messages from "../views/Messages.vue";
import FindConnection from "../views/FindConnection.vue";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: "/messages",
    name: "Messages",
    component: Messages,
    beforeEnter: (to, from, next) => {
      if (store.state.user.accessToken == null) next({ name: 'SignIn' });
      else next();
    },
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    beforeEnter: (to, from, next) => {
      if (store.state.user.accessToken == null) next({ name: 'SignIn' });
      else next();
    },
  },
  {
    path: "/find-connection",
    name: "FindConnection",
    component: FindConnection,
    beforeEnter: (to, from, next) => {
      if (store.state.user.accessToken == null) next({ name: 'SignIn' });
      else next();
    },
  },
  {
    path: "/sign-in",
    name: "SignIn",
    component: SignIn,
    beforeEnter: (to, from, next) => {
      if (store.state.user.accessToken != null) next({ name: 'Home' });
      else next();
    },
  },
  {
    path: "/sign-up",
    name: "SignUp",
    component: SignUp,
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
