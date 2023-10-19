<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="8" class="ml-auto mr-auto">
        <div class="text-center">
          <ChangeProfile />

          <hr class="hr-element" />

          <!-- username and email -->
          <UpdateUsernameEmail />

          <hr class="hr-element" />

          <!--change password  -->
          <ChangePassword />

          <hr class="hr-element" />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import UpdateUsernameEmail from "../components/UpdateUsernameEmail.vue";
import ChangePassword from "../components/ChangePassword.vue";
import ChangeProfile from "../components/ChangeProfile.vue";

export default {
  name: "Profile",

  components: {
    UpdateUsernameEmail,
    ChangePassword,
    ChangeProfile,
  },

  data: () => ({
    showPassword: false,

    oldPassword: "",
    newPassword: "",
    confirmNewPassword: "",

    errOldPassword: "",
    errNewPassword: "",

    changePasswordSuccess: false,
  }),

  methods: {},
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