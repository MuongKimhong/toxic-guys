import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'

Vue.use(Vuex)

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
});

export default new Vuex.Store({
  state: {
    webSocketServer: "http://localhost:3000",

    user: {
      id: null,
      username: null,
      profileUrl: null,
      acceptAnonymousMessage: null,
      accessToken: null
    }
  },
  getters: {
  },
  mutations: {
    updateUserCredential(state, credential) {
      state.user.id = credential.id;
      state.user.username = credential.username;
      state.user.profileUrl = credential.profile_url;
      state.user.acceptAnonymousMessage = credential.accept_anonymous_message;
      state.user.accessToken = credential.access_token;
    },

    updateOnlyUserProfileUrl(state, newUrl) {
      state.user.profileUrl = newUrl;
    },

    deleteUserCredential(state) {
      state.user = {
        id: null,
        username: null,
        profileUrl: null,
        acceptAnonymousMessage: null,
        accessToken: null
      }
    }
  },
  actions: {
  },
  modules: {
  },
  plugins: [vuexLocal.plugin]
})
