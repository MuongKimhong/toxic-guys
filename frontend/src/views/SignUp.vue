<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="8" class="mr-auto ml-auto">
        <div>
          <v-card
            class="px-12 py-9 white--text"
            style="background-color: rgb(95, 95, 95); border-radius: 8px"
          >
            <h1 class="text-center">Sign Up</h1>

            <div class="mt-10">
              <v-text-field
                class="my-1"
                dense
                label="username"
                dark
                outlined
                v-model="username"
                :error-messages="error.username"
              ></v-text-field>
              <v-text-field
                class="my-1"
                dense
                label="email address"
                dark
                outlined
                v-model="email"
                :error-messages="error.email"
                type="email"
              ></v-text-field>
              <v-text-field
                password
                class="my-"
                dense
                label="password"
                dark
                outlined
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                v-model="password"
                :error-messages="error.password"
              >
              </v-text-field>
              <v-text-field
                password
                class="my-"
                dense
                label="confirm password"
                dark
                outlined
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                v-model="confirmPassword"
                :error-messages="error.confirmPassword"
              >
              </v-text-field>
            </div>

            <div class="mt-5 text-center mr-auto ml-auto">
              <v-btn
                id="signup-btn"
                class="text-capitalize white--text"
                style="background-color: rgb(78, 78, 78)"
                @click="signUp()"
              >
                Sign Up
              </v-btn>
            </div>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "SignUp",

  data: () => ({
    showPassword: false,
    username: "",
    email: "",
    password: "",
    confirmPassword: "",

    error: {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  }),

  created() {
    document.addEventListener("keyup", (event) => {
      if (event.key === "Enter") {
        document.getElementById("signup-btn").click();
      }
    });
  },

  methods: {
    comparePassword: function () {
      if (this.password != this.confirmPassword) {
        this.error.password = "Two password did not match";
        this.error.confirmPassword = "Two password did not match";
        return false;
      }
      return true;
    },

    checkIfCredentialsEmpty: function () {
      if (this.username.trim() === "") {
        this.error.username = "Username is required to sign up!";
        return false;
      } else if (this.email.trim() === "") {
        this.error.email = "Email is required to sign up!";
        return false;
      } else if (
        this.password.trim() === "" ||
        this.confirmPassword.trim() === ""
      ) {
        this.error.password = "Please enter password!";
        this.error.confirmPassword = "Please enter password!";
        return false;
      }
      return true;
    },

    reInitializeErrorMessage: function () {
      this.error = {
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
      };
    },

    signUp: function () {
      this.reInitializeErrorMessage();

      if (
        this.comparePassword() === false ||
        this.checkIfCredentialsEmpty() === false
      ) {
        setTimeout(() => this.reInitializeErrorMessage(), 2000);
        return false;
      }

      axios
        .post("api-users/sign-up/", {
          username: this.username,
          email: this.email,
          password: this.password,
          confirm_password: this.confirmPassword,
        })
        .then(async (res) => {
          if (res.data["signup_success"]) {
            // global function in main.js
            let response = await this.$authenticateUser(
              this.username,
              this.password
            );

            if (response === false) this.$router.push({ name: "SignIn" });
          }
        })
        .catch((err) => {
          if (err.response.data["two_password_not_match"]) {
            this.error.password = "Two password did not match";
            this.error.confirmPassword = "Two password did not match";
          } else if (err.response.data["weak_password"]) {
            this.error.password = err.response.data["weak_password"];
            this.error.confirmPassword = err.response.data["weak_password"];
          } else if (err.response.data["email_taken"]) {
            this.error.email = "Email address is already taken";
          } else if (err.response.data["username_taken"]) {
            this.error.username = "Username is already taken";
          }
        });
    },
  },
};
</script>