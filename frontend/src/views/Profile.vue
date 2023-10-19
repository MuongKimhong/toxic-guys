<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="8" class="ml-auto mr-auto">
        <div class="text-center">
          <v-avatar size="160" color="white" class="ml-auto mr-auto"></v-avatar>
          <div class="mt-5">
            <v-btn
              class="text-capitalize white--text"
              style="background-color: rgb(95, 95, 95)"
              small
            >
              Change profile
            </v-btn>
          </div>

          <hr class="hr-element" />

          <!-- username and email -->
          <div class="mt-5 px-12">
            <h3 class="text-center mb-5">Username & Email address</h3>
            <v-text-field
              class="my-2"
              dense
              label="Username"
              dark
              outlined
              v-model="username"
              :error-messages="errUsername"
            ></v-text-field>
            <v-text-field
              class="my-2"
              dense
              label="Email address"
              dark
              outlined
              v-model="email"
              :error-messages="errEmail"
            ></v-text-field>

            <div>
              <v-btn
                small
                class="white--text text-capitalize"
                style="background-color: rgb(95, 95, 95)"
                @click="updateUsernameAndEmail()"
              >
                Update
              </v-btn>
            </div>
          </div>

          <hr class="hr-element" />

          <div class="mt-5 px-12 pb-12">
            <h3 class="text-center mb-5">Change password</h3>
            <v-text-field
              password
              class="my-2"
              dense
              label="Old password"
              dark
              outlined
              :type="showPassword ? 'text' : 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
            >
            </v-text-field>
            <v-text-field
              password
              class="my-2"
              dense
              label="New password"
              dark
              outlined
              :type="showPassword ? 'text' : 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
            >
            </v-text-field>
            <v-text-field
              password
              class="my-2"
              dense
              label="Confirm new password"
              dark
              outlined
              :type="showPassword ? 'text' : 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
            >
            </v-text-field>

            <div>
              <v-btn
                small
                class="white--text text-capitalize"
                style="background-color: rgb(95, 95, 95)"
              >
                Change
              </v-btn>
            </div>

            <hr class="hr-element" />
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Profile",

  data: () => ({
    showPassword: false,

    username: "",
    email: "",

    errUsername: "",
    errEmail: "",
  }),

  created() {
    this.email = this.$store.state.user.email;
    this.username = this.$store.state.user.username;
  },

  methods: {
    updateUsernameAndEmail: function () {
      this.errUsername = "";
      this.errEmail = "";

      if (
        this.username == this.$store.state.user.username &&
        (this.email = this.$store.state.user.email)
      ) {
        return;
      }

      axios
        .post(
          "api-users/update-email-username/",
          {
            email: this.email,
            username: this.username,
          },
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          }
        )
        .then((res) => {
          if (res.data["success"]) {
            this.$store.commit("updateOnlyUsernameAndEmail", {
              email: this.email,
              username: this.username,
            });
            this.$updateToken(res.data["new_token"]);
          }
        })
        .catch((err) => {
          if (err.response.data["username_error"]) {
            this.errUsername = err.response.data["username_error"];
          }
          if (err.response.data["email_error"]) {
            this.errEmail = err.response.data["email_error"];
          }
        });
    },
  },
};
</script>

<style scoped>
.hr-element {
  background-color: grey;
  height: 1px;
  border: none;
  margin-top: 50px;
  margin-bottom: 50px;
}
</style>