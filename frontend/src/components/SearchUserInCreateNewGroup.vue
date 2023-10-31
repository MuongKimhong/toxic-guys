<template>
  <v-card
    v-if="showSearchUsers === true"
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
          <tbody v-if="connections.length > 0">
            <tr>
              <td>
                <span class="ml-2"> Hell </span>
              </td>
              <td class="text-right">
                <v-btn small class="dark-grey white--text text-capitalize">
                  Connect
                </v-btn>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </div>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchUserInCreateNewGroup",
  props: ["showSearchUsers", "groupType"],

  data: () => ({
    connections: [],
    randomUsers: [],
    currentPage: 1,
    totalPages: 0,
  }),

  watch: {
    groupType: function (newValue, oldValue) {
      // watch it
      console.log(newValue, oldValue);
    },
  },

  methods: {
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
            // this.connections = res.data["connections"];
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
            // this.randomUsers = res.data["random_users"];
            // this.totalPages = res.data["total_pages"];
          }
        });
    },
  },
};
</script>

