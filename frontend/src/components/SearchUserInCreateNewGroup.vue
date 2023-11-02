<template>
  <v-card
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
      @keyup="typingSearchHandling()"
      v-model="searchText"
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
          <tbody>
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
                <v-btn small class="dark-grey white--text text-capitalize">
                  Invite
                </v-btn>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>

      <div class="text-right mt-5">
        <v-btn
          v-if="currentPage > 1 && currentPage <= totalPages"
          x-small
          class="text-capitalize mr-1"
          @click="previousPageButtonOnClick()"
        >
          Previous
        </v-btn>
        <v-btn
          v-if="currentPage >= 1 && currentPage < totalPages"
          x-small
          class="text-capitalize ml-1"
          @click="nextPageButtonOnClick()"
        >
          Next >
        </v-btn>
      </div>
    </div>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchUserInCreateNewGroup",
  props: ["showSearchUsers", "groupType"],

  data: () => ({
    randomUsers: [],
    currentPage: 1,
    totalPages: 0,
    searchText: "",
  }),

  watch: {
    groupType: function (newValue) {
      // watch it
      if (newValue === "Public" || newValue === "Private") {
        if (this.randomUsers.length == 0) this.getRandomUsers();
      }
    },
  },

  methods: {
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

            console.log(this.randomUsers);
          }
        });
    },

    nextPageButtonOnClick: function () {
      this.currentPage = this.currentPage + 1;

      if (this.searchText.trim() === "") this.getRandomUsers();
      else this.searchUsers();
    },

    previousPageButtonOnClick: function () {
      this.currentPage = this.currentPage - 1;

      if (this.searchText.trim() === "") this.getRandomUsers();
      else this.searchUsers();
    },

    searchUsers: function () {
      if (this.searchText.trim() != "") {
        axios
          .get("api-users/search-users/", {
            params: {
              search_text: this.searchText,
              page: this.currentPage,
            },
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          })
          .then((res) => {
            if (res.data["results"]) {
              this.randomUsers = res.data["results"];
              this.totalPages = res.data["total_pages"];
            }
          });
      } else {
        this.getRandomUsers();
      }
    },

    typingSearchHandling: function () {
      this.currentPage = 1;
      this.searchUsers();
    },
  },
};
</script>

