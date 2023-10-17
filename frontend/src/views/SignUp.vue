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
              ></v-text-field>
              <v-text-field
                class="my-1"
                dense
                label="email address"
                dark
                outlined
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
              >
              </v-text-field>
            </div>

            <div class="mt-5 text-center mr-auto ml-auto">
              <v-btn
                class="text-capitalize white--text"
                style="background-color: rgb(78, 78, 78)"
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
export default {
  name: "SignUp",
  data: () => ({
    showPassword: false,
  }),
};
</script>