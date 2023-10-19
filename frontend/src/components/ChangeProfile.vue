<template>
  <div>
    <v-avatar size="160" color="white" class="ml-auto mr-auto">
      <v-img
        v-if="profile == ''"
        :src="require(`../../public/userimg.png`)"
      ></v-img>
      <v-img v-else :src="profile"></v-img>
    </v-avatar>
    <div class="mt-5">
      <v-btn
        v-if="newProfile === null"
        class="text-capitalize white--text"
        style="background-color: rgb(95, 95, 95)"
        small
        @click="changeProfileBtnOnClick()"
      >
        Change profile
      </v-btn>
      <v-btn
        v-else
        class="text-capitalize white--text"
        style="background-color: green"
        small
        @click="changeProfile()"
      >
        Save image
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ChangeProfile",

  data: () => ({
    profile: "",
    newProfile: null,
  }),

  created() {
    this.profile = this.$store.state.user.profileUrl;
  },

  methods: {
    changeProfile: function () {
      var formData = new FormData();
      formData.append("profile", this.newProfile);
      axios
        .post("api-users/change-profile/", formData, {
          headers: {
            "content-type": "multipart/form-data",
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          if (res.data["profile"]) {
            this.$store.commit("updateOnlyUserProfileUrl", res.data["profile"]);
            this.profile = res.data["profile"];
            this.newProfile = null;
            this.$updateToken(res.data["new_token"]);
          }
        });
    },

    changeProfileBtnOnClick: function () {
      let self = this;
      let input = document.createElement("input");
      input.type = "file";
      input.accept = ".jpg,.JPEG,.png";
      input.onchange = () => {
        let files = Array.from(input.files);
        self.newProfile = files[0];
        self.profile = URL.createObjectURL(files[0]);
      };
      input.click();
    },
  },
};
</script>