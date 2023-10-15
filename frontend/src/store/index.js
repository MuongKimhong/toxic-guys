import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'

Vue.use(Vuex)

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
});

export default new Vuex.Store({
  state: {
    webSocketServer: "http://localhost:3000"
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
