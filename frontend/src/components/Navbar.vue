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
          <v-badge
            v-if="totalUnSeenNotification > 0"
            :content="totalUnSeenNotification"
            color="error"
          >
            <i class="fas fa-bell white--text"></i>
          </v-badge>
          <i v-else class="fas fa-bell white--text"></i>
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
          <v-list v-if="notifications.length > 0">
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
                  <v-btn
                    x-small
                    class="text-capitalize white--text red mr-2"
                    @click="
                      acceptOrRejectConnectionRequest(
                        notification,
                        index,
                        (accept = false),
                        (reject = true)
                      )
                    "
                  >
                    Reject
                  </v-btn>
                  <v-btn
                    x-small
                    class="text-capitalize white--text green ml-2"
                    @click="
                      acceptOrRejectConnectionRequest(
                        notification,
                        index,
                        (accept = true),
                        (reject = false)
                      )
                    "
                  >
                    Accept
                  </v-btn>
                </div>
              </v-list-item-title>

              <v-list-item-title
                v-else-if="notification.type == 'connection-accept'"
              >
                <v-avatar size="26" color="white">
                  <v-img
                    v-if="notification.sender.profile_url == ''"
                    :src="require('../../public/userimg.png')"
                  ></v-img>
                  <v-img v-else :src="notification.sender.profile_url"></v-img>
                </v-avatar>

                <span class="ml-2">{{ notification.text }}</span>
              </v-list-item-title>

              <v-list-item-title
                v-else-if="
                  notification.type == 'group_invitation' &&
                  notification.group_invitation != null
                "
              >
                <v-avatar size="26" color="white">
                  <v-img
                    v-if="notification.sender.profile_url == ''"
                    :src="require('../../public/userimg.png')"
                  ></v-img>
                  <v-img v-else :src="notification.sender.profile_url"></v-img>
                </v-avatar>

                <span class="ml-2">{{ notification.text }}</span>

                <div
                  v-if="notification.group_invitation.accepted == false"
                  class="mt-3 text-center"
                >
                  <v-btn
                    x-small
                    class="text-capitalize white--text red mr-2"
                    @click="
                      acceptOrDeleteGroupInvitation(
                        notification,
                        index,
                        (accept = false),
                        (reject = true)
                      )
                    "
                  >
                    Delete
                  </v-btn>
                  <v-btn
                    x-small
                    class="text-capitalize white--text green ml-2"
                    @click="
                      acceptOrDeleteGroupInvitation(
                        notification,
                        index,
                        (accept = true),
                        (reject = false)
                      )
                    "
                  >
                    Join
                  </v-btn>
                </div>
              </v-list-item-title>
            </v-list-item>
          </v-list>
          <v-list v-else class="text-center mt-5"> No notifications </v-list>
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
    totalUnSeenNotification: 0, // number of notification that haven't seen by receiver
  }),

  created() {
    if (this.$store.state.user.accessToken != null) {
      this.listenToWebSocketEventHandling();
      this.getNumberOfUnseenNotifications();
    }
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

              this.markNotificationAsSeenByReceiver(); // after open notifications, mark all as seen
            }
          });
      } else {
        this.showNotificationDialog = true;
      }
    },

    getNumberOfUnseenNotifications: function () {
      axios
        .get("api-notifications/get-number-of-unseen-notifications/", {
          headers: {
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          if (res.data["total_unseen"]) {
            this.totalUnSeenNotification = res.data["total_unseen"];
          }
        });
    },

    notificationBtnOnClick: function () {
      if (this.showNotificationDialog == false) this.getNotifications();
      else this.showNotificationDialog = false;
    },

    listenToWebSocketEventHandling: function () {
      this.$webSocket.on("connection-request", (userToBeConnectedId) => {
        if (this.$store.state.user.id == userToBeConnectedId) {
          if (this.showNotificationDialog == false) {
            this.totalUnSeenNotification = this.totalUnSeenNotification + 1;
          } else if (this.showNotificationDialog == true) {
            this.getNotifications();
          }
        }
      });

      this.$webSocket.on("accepted", (requestSenderId) => {
        if (this.$store.state.user.id == requestSenderId) {
          if (this.showNotificationDialog == false) {
            this.totalUnSeenNotification = this.totalUnSeenNotification + 1;
          } else if (this.showNotificationDialog == true) {
            this.getNotifications();
          }
        }
      });

      this.$webSocket.on("group-invitation-sent", (invitedUserIds) => {
        var ids = JSON.parse(invitedUserIds);

        if (ids.includes(this.$store.state.user.id) === true) {
          if (this.showNotificationDialog == false) {
            this.totalUnSeenNotification = this.totalUnSeenNotification + 1;
          } else if (this.showNotificationDialog == true) {
            this.getNotifications();
          }
        }
      });
    },

    acceptOrRejectConnectionRequest: function (
      notificationObj,
      index,
      accept = false,
      reject = false
    ) {
      if (accept === false && reject === false) {
        return;
      }
      var status = "";

      if (accept === true) status = "accept";
      else if (reject === true) status = "reject";

      axios
        .post(
          "api-users/accept-or-reject-connection-request/",
          {
            request_sender_id: notificationObj.sender.id,
            response: status,
            notification_id: notificationObj.id,
          },
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          }
        )
        .then((res) => {
          if (res.data) this.notifications.splice(index, 1);

          if (res.data["accepted"] === true) {
            this.$webSocket.emit(
              "connection-accepted",
              notificationObj.sender.id
            );
          }
        })
        .catch(() => {});
    },

    acceptOrDeleteGroupInvitation: function (
      notificationObj,
      index,
      accept = false,
      reject = false
    ) {
      if (accept === false && reject === false) {
        return;
      }

      if (accept === true) {
        axios
          .post(
            "api-groups/accept-group-invitation/",
            {
              group_invitation_id: notificationObj.group_invitation.id,
            },
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.user.accessToken}`,
              },
            }
          )
          .then((res) => {
            if (res.data["accept"]) {
              this.notifications[index]["group_invitation"]["accepted"] = true;
            }
          })
          .catch((res) => {
            console.log(res);
          });
      }

      if (reject === true) {
        axios
          .post(
            "api-groups/delete-group-invitation/",
            {
              group_invitation_id: notificationObj.group_invitation.id,
            },
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.user.accessToken}`,
              },
            }
          )
          .then((res) => {
            if (res.data["delete"]) {
              this.notifications.splice(index, 1);
            }
          })
          .catch((res) => {
            console.log(res);
          });
      }
    },

    markNotificationAsSeenByReceiver: function () {
      axios
        .post(
          "api-notifications/mark-notification-as-seen-by-receiver/",
          {},
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          }
        )
        .then((res) => {
          if (res.data["seen_all"]) {
            this.totalUnSeenNotification = 0;
          }
        });
    },
  },
};
</script>

<style scoped>
.navbar-color {
  background-color: rgb(95, 95, 95);
}
</style>