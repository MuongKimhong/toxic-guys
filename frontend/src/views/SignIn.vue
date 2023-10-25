<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="8" class="mr-auto ml-auto">
        <div>
          <v-card
            class="px-12 py-9 white--text"
            style="background-color: rgb(95, 95, 95); border-radius: 8px"
          >
            <h1 class="text-center">Sign In</h1>

            <div class="mt-10">
              <v-text-field
                class="my-2"
                dense
                label="username"
                dark
                outlined
                v-model="username"
                :error-messages="errorMessage"
              ></v-text-field>
              <v-text-field
                password
                class="my-2"
                dense
                label="password"
                dark
                outlined
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                v-model="password"
                :error-messages="errorMessage"
              >
              </v-text-field>
            </div>

            <div class="mt-5 text-center mr-auto ml-auto">
              <v-btn
                id="signin-btn"
                class="text-capitalize white--text"
                style="background-color: rgb(78, 78, 78)"
                @click="signIn()"
              >
                Sign In
              </v-btn>

              <div class="mt-4">
                <small>
                  Need an account?
                  <a
                    @click="$router.push({ name: 'SignUp' })"
                    style="color: white"
                  >
                    Sign Up
                  </a>
                </small>
              </div>
            </div>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "SignIn",

  data: () => ({
    showPassword: false,

    username: "",
    password: "",
    errorMessage: "",
  }),

  created() {
    document.addEventListener("keyup", (event) => {
      if (event.key === "Enter") {
        document.getElementById("signin-btn").click();
      }
    });
  },

  methods: {
    signIn: async function () {
      this.errorMessage = "";

      if (this.username.trim() === "" || this.password.trim() === "") {
        this.errorMessage = "Please enter username and password";
      }

      let response = await this.$authenticateUser(this.username, this.password);

      if (response === false) {
        this.errorMessage = "Username or password is incorrect";

        setTimeout(() => {
          this.errorMessage = "";
        }, 2000);
      }
    },
  },
};
</script>

<style scoped>
</style>