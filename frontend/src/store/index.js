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
      email: null,
      profileUrl: null,
      acceptAnonymousMessage: null,
      accessToken: null,
      refreshToken: null
    }
  },
  getters: {
  },
  mutations: {
    updateUserCredential(state, credential) {
      state.user.id = credential.user.id;
      state.user.username = credential.user.username;
      state.user.email = credential.user.email;
      state.user.profileUrl = credential.user.profile_url;
      state.user.acceptAnonymousMessage = credential.user.accept_anonymous_message;
      state.user.accessToken = credential.access_token;
      state.user.refreshToken = credential.refresh_token;
    },

    updateOnlyUserToken(state, tokenObject) {
      state.user.accessToken = tokenObject.access_token;
      state.user.refreshToken = tokenObject.refresh_token;
    },

    updateOnlyUsernameAndEmail(state, data) {
      state.user.username = data.username;
      state.user.email = data.email;
    },

    updateOnlyUserProfileUrl(state, newUrl) {
      state.user.profileUrl = newUrl;
    },

    deleteUserCredential(state) {
      state.user = {
        id: null,
        username: null,
        email: null,
        profileUrl: null,
        acceptAnonymousMessage: null,
        accessToken: null,
        refreshToken: null
      }
    }
  },
  actions: {
  },
  modules: {
  },
  plugins: [vuexLocal.plugin]
})
