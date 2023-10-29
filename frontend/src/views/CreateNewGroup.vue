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

            <v-card
              v-if="showConnections || showRandomUsers"
              style="background-color: rgb(75, 75, 75)"
              class="px-5 py-6"
              elevation="8"
            >
              <v-text-field
                dark
                label="Search users"
                dense
                outlined
                append-icon="mdi-account-search"
              ></v-text-field>

              <div>
                <v-simple-table
                  style="background-color: rgb(95, 95, 95)"
                  dark
                  class="white--text"
                >
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-left white--text">Users</th>
                        <th class="text-left white--text"></th>
                      </tr>
                    </thead>
                    <tbody v-if="showConnections === true">
                      <tr
                        v-for="(connection, index) in connections"
                        :key="index"
                      >
                        <td>
                          <v-avatar size="28" color="white">
                            <v-img
                              v-if="connection.connection.profile_url == ''"
                              :src="require('../../public/userimg.png')"
                            ></v-img>
                            <v-img
                              v-else
                              :src="connection.connection.profile_url"
                            ></v-img>
                          </v-avatar>
                          <span class="ml-2">
                            {{ connection.connection.username }}
                          </span>
                        </td>
                        <td class="text-right">
                          <v-btn
                            small
                            class="dark-grey white--text text-capitalize"
                          >
                            Connect
                          </v-btn>
                        </td>
                      </tr>
                    </tbody>
                    <tbody v-if="showRandomUsers === true">
                      <tr v-for="(user, index) in randomUsers" :key="index">
                        <td v-if="user.id != $store.state.user.id">
                          <v-avatar size="28" color="white">
                            <v-img
                              v-if="user.profile_url == ''"
                              :src="require('../../public/userimg.png')"
                            ></v-img>
                            <v-img v-else :src="user.profile_url"></v-img>
                          </v-avatar>
                          <span class="ml-2">{{ user.username }}</span>
                        </td>
                        <td class="text-right">
                          <v-btn
                            small
                            class="dark-grey white--text text-capitalize"
                          >
                            Connect
                          </v-btn>
                        </td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </div>
            </v-card>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "CreateNewGroup",

  data: () => ({
    groupImage: null,
    groupImageURL: null,
    groupName: "",
    groupType: "",

    connections: [], //friend
    randomUsers: [],

    currentPage: 1,
    totalPages: 0,

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
      console.log(this.groupType);

      if (this.groupType === "Private") {
        this.getAllConnections();
        this.showRandomUsers = false;
        this.showConnections = true;
      } else if (this.groupType === "Public") {
        this.getRandomUsers();
        this.showConnections = false;
        this.showRandomUsers = true;
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