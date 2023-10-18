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
            ></v-text-field>
            <v-text-field
              class="my-2"
              dense
              label="Email address"
              dark
              outlined
            ></v-text-field>

            <div>
              <v-btn
                small
                class="white--text text-capitalize"
                style="background-color: rgb(95, 95, 95)"
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
export default {
  name: "Profile",

  data: () => ({
    showPassword: false,
  }),
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