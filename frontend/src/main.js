import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'

axios.defaults.baseURL = "http://localhost:8000/"

Vue.config.productionTip = false

Vue.prototype.$authenticateUser = async function (username, password) {
  try {
    let response = await axios.post("api-users/sign-in/", {
      username: username,
      password: password
    });

    store.commit("updateUserCredential", response.data);

    // make sure store.commit finish operation
    setTimeout(() => {
      router.push({ name: "Home" })
    }, 200)

    return true;

  } catch (error) {
    if (error.response) return false;
  }
}

Vue.prototype.$updateToken = function (newToken) {
  store.commit("updateOnlyUserToken", newToken);
}

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
