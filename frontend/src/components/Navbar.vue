<template>
  <div>
    <v-app-bar
      app
      class="white--text"
      height="100"
      style="background-color: rgb(95, 95, 95)"
    >
      <div
        class="d-flex align-center"
        @click="$router.push({ name: 'Home' })"
        style="cursor: pointer"
      >
        <h1>ToxicGuys</h1>
      </div>

      <v-spacer></v-spacer>

      <!-- signed in -->
      <div v-if="$store.state.user.accessToken != null">
        <v-btn text @click="$router.push({ name: 'Messages' })">
          <span class="text-capitalize mr-1 white--text">Messages</span>
          <i class="fas fa-comments white--text"></i>
        </v-btn>
        <v-btn text>
          <span class="text-capitalize mr-1 white--text">Anonymous</span>
          <i class="fas fa-question white--text"></i>
        </v-btn>
        <v-btn text @click="notificationBtnOnClick()" id="notification-btn">
          <span class="text-capitalize mr-1 white--text"> Notifications </span>
          <i class="fas fa-bell white--text"></i>
        </v-btn>
        <v-btn text @click="$router.push({ name: 'Profile' })">
          <span class="text-capitalize mr-1 white--text">Profile</span>
          <i class="fas fa-user-circle white--text"></i>
        </v-btn>
        <v-btn text @click="signOut()">
          <span class="text-capitalize mr-1 white--text">Sign Out</span>
          <i class="fas fa-sign-out-alt white--text"></i>
        </v-btn>
      </div>

      <v-dialog v-model="showNotificationDialog" width="350" height="450">
        <v-card class="py-2 px-2 white--text" width="350" height="450" dark>
          <v-list>
            <v-list-item
              v-for="(notification, index) in notifications"
              :key="index"
            >
              <v-list-item-title v-if="notification.type == 'connection'">
                <v-avatar size="26" color="white">
                  <v-img
                    v-if="notification.sender.profile_url == ''"
                    :src="require('../../public/userimg.png')"
                  ></v-img>
                  <v-img v-else :src="notification.sender.profile_url"></v-img>
                </v-avatar>

                <span class="ml-2">{{ notification.text }}</span>

                <div class="mt-3 text-center">
                  <v-btn x-small class="text-capitalize white--text red mr-2">
                    Reject
                  </v-btn>
                  <v-btn x-small class="text-capitalize white--text green ml-2">
                    Accept
                  </v-btn>
                </div>
              </v-list-item-title>

              <v-list-item-title v-else>Hello</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-dialog>

      <!-- not signed in -->
      <div
        v-if="$store.state.user.accessToken == null && $route.name != 'SignIn'"
      >
        <v-btn text @click="$router.push({ name: 'SignIn' })">
          <span class="text-capitalize white--text">Sign In </span>
        </v-btn>
      </div>
    </v-app-bar>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Navbar",

  data: () => ({
    showNotificationDialog: false,

    notifications: [],
  }),

  created() {
    this.$webSocket.on("connection-request", (userToBeConnectedId) => {
      if (this.$store.state.user.id == userToBeConnectedId) {
        console.log("new connection notification");
      }
    });
  },

  methods: {
    signOut: function () {
      axios
        .post(
          "api-users/sign-out/",
          {
            refresh_token: this.$store.state.user.refreshToken,
          },
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          }
        )
        .then((res) => {
          this.$store.commit("deleteUserCredential");
          if (res.data["success"]) {
            this.$router.push({ name: "SignIn" });
          }
        })
        .catch(() => {});
    },

    getNotifications: function () {
      if (this.notifications.length == 0) {
        axios
          .get("api-notifications/get-all-notifications/", {
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          })
          .then((res) => {
            if (res.data["notifications"]) {
              this.notifications = res.data["notifications"];
              this.showNotificationDialog = true;
            }
          });
      } else {
        this.showNotificationDialog = true;
      }
    },

    notificationBtnOnClick: function () {
      if (this.showNotificationDialog == false) this.getNotifications();
      else this.showNotificationDialog = false;
    },
  },
};
</script>

<style scoped>
.navbar-color {
  background-color: rgb(95, 95, 95);
}
</style>