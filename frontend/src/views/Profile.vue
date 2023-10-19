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
            <h4
              v-if="changePasswordSuccess == true"
              class="text-center green--text mb-5"
            >
              Password is changed
            </h4>
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
              v-model="oldPassword"
              :error-messages="errOldPassword"
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
              v-model="newPassword"
              :error-messages="errNewPassword"
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
              v-model="confirmNewPassword"
              :error-messages="errNewPassword"
            >
            </v-text-field>

            <div>
              <v-btn
                small
                class="white--text text-capitalize"
                style="background-color: rgb(95, 95, 95)"
                @click="changePassword()"
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

    oldPassword: "",
    newPassword: "",
    confirmNewPassword: "",

    errUsername: "",
    errEmail: "",

    errOldPassword: "",
    errNewPassword: "",

    changePasswordSuccess: false,
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

    changePassword: function () {
      this.errOldPassword = "";
      this.errNewPassword = "";
      this.changePasswordSuccess = false;

      if (this.oldPassword.trim() === "")
        this.errOldPassword = "Please enter old password";
      else if (
        this.newPassword.trim() === "" ||
        this.confirmNewPassword.trim() === ""
      ) {
        this.errNewPassword = "Please enter new password";
      } else if (this.newPassword != this.confirmNewPassword) {
        this.errNewPassword = "Two passwords did not match";
      } else {
        axios
          .post(
            "api-users/change-password/",
            {
              old_password: this.oldPassword,
              new_password: this.newPassword,
            },
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.user.accessToken}`,
              },
            }
          )
          .then((res) => {
            if (res.data["success"]) {
              this.$updateToken(res.data["new_token"]);
              this.changePasswordSuccess = true;

              setTimeout(() => {
                this.changePasswordSuccess = false;
              }, 1000);

              this.errOldPassword = "";
              this.errNewPassword = "";
            }
          })
          .catch((err) => {
            if (err.response.data["old_password_error"]) {
              this.errOldPassword = err.response.data["old_password_error"];
            } else if (err.response.data["weak_password"]) {
              this.errNewPassword = err.response.data["weak_password"];
            }
          });
      }
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