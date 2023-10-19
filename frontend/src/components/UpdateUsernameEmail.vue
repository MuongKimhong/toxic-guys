<template>
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
</template>

<script>
import axios from "axios";

export default {
  name: "UpdateUsernameEmail",

  data: () => ({
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