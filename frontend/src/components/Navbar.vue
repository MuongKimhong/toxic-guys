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

      <v-menu
        v-model="showNotificationMenu"
        absolute
        :min-width="notificationMenu.width"
        :position-x="notificationMenu.positionX"
        :position-y="notificationMenu.positionY"
      >
        <v-list v-if="notifications.length > 0">
          <v-list-item
            v-for="(notification, index) in notifications"
            :key="index"
          >
            <v-list-item-title>
              {{ notification.text }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
        <v-list v-else>
          <v-list-item>
            <v-list-item-title>No new notifications</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

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
    showNotificationMenu: false,
    notificationMenu: {
      width: 300,
      positionX: null,
      positionY: null,
    },

    notifications: [],
  }),

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
              this.showNotificationMenu = true;
            }
          });
      } else {
        this.showNotificationMenu = true;
      }
    },

    notificationBtnOnClick: function () {
      let btnElement = document.getElementById("notification-btn");
      let rect = btnElement.getBoundingClientRect();
      this.notificationMenu["positionX"] = rect.left;
      this.notificationMenu["positionY"] = rect.top + 50;
      if (this.showNotificationMenu == false) this.getNotifications();
      else this.showNotificationMenu = false;
    },
  },
};
</script>

<style scoped>
.navbar-color {
  background-color: rgb(95, 95, 95);
}
</style>