<template>
  <v-container>
    <v-row align="center" justify-content="center">
      <v-col cols="8" class="mr-auto ml-auto">
        <div>
          <div class="text-center">
            <v-avatar size="120" color="white" class="ml-auto mr-auto">
              <v-img
                v-if="groupImage === null"
                :src="require(`../../public/groupimg.png`)"
              ></v-img>
              <v-img v-else :src="groupImageURL"></v-img>
            </v-avatar>

            <div class="text-center mt-5">
              <v-btn
                v-if="groupImage === null"
                small
                class="text-capitalize white--text"
                style="background-color: rgb(95, 95, 95)"
                @click="uploadImageBtnOnClick()"
              >
                Upload Image
              </v-btn>
              <v-btn
                v-else
                small
                class="text-capitalize white--text"
                style="background-color: rgb(95, 95, 95)"
                @click="uploadImageBtnOnClick()"
              >
                Change Image
              </v-btn>
            </div>
          </div>

          <div class="mt-10">
            <v-text-field
              dark
              label="Group name"
              dense
              outlined
              rounded
              counter="30"
              v-model="groupName"
            ></v-text-field>

            <v-select
              :items="['Public', 'Private']"
              density="compact"
              dense
              label="Group type"
              dark
              outlined
              rounded
              v-model="groupType"
              @change="groupTypeOnChange()"
            ></v-select>

            <SearchUserInCreateNewGroup
              :showSearchUsers="showSearchUsers"
              :groupType="groupType"
            />
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

import SearchUserInCreateNewGroup from "../components/SearchUserInCreateNewGroup.vue";

export default {
  name: "CreateNewGroup",

  components: {
    SearchUserInCreateNewGroup,
  },

  data: () => ({
    groupImage: null,
    groupImageURL: null,
    groupName: "",
    groupType: "",

    connections: [], //friend
    randomUsers: [],

    currentPage: 1,
    totalPages: 0,

    showSearchUsers: false,
    showConnections: true,
    showRandomUsers: false,
  }),

  methods: {
    uploadImageBtnOnClick: function () {
      let self = this;
      let input = document.createElement("input");
      input.type = "file";
      input.accept = ".jpg,.JPEG,.png";
      input.onchange = () => {
        let files = Array.from(input.files);
        self.groupImage = files[0];
        self.groupImageURL = URL.createObjectURL(files[0]);
        input.remove();
      };
      input.click();
    },

    groupTypeOnChange: function () {
      if (this.groupType === "Private" || this.groupType === "Public") {
        this.showSearchUsers = true;
      } else {
        this.showSearchUsers = false;
      }
    },

    // get all friends
    getAllConnections: function () {
      if (this.connections.length > 0) return;

      axios
        .get("api-users/get-all-connections/", {
          headers: {
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          if (res.data["connections"]) {
            this.connections = res.data["connections"];
          }
        });
    },

    getRandomUsers: function () {
      axios
        .get("api-users/get-random-users/", {
          params: {
            page: this.currentPage,
          },
          headers: {
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          if (res.data["random_users"]) {
            this.randomUsers = res.data["random_users"];
            this.totalPages = res.data["total_pages"];
          }
        });
    },
  },
};
</script>