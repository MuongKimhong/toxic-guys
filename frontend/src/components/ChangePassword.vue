<template>
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
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ChangePassword",

  data: () => ({
    showPassword: false,

    oldPassword: "",
    newPassword: "",
    confirmNewPassword: "",

    errOldPassword: "",
    errNewPassword: "",

    changePasswordSuccess: false,
  }),

  methods: {
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
              this.oldPassword = "";
              this.newPassword = "";
              this.confirmNewPassword = "";

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