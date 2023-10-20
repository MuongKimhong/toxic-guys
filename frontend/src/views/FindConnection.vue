<template>
  <v-container>
    <SearchUser />

    <div class="mt-5">
      <v-card style="background-color: rgb(95, 95, 95)" class="white--text">
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
              <tr v-for="user in users" :key="user.id">
                <td>
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
                    Connect
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import SearchUser from "../components/SearchUser.vue";

export default {
  name: "FindConnection",

  components: {
    SearchUser,
  },

  data: () => ({
    users: [],
  }),

  created() {
    this.getRandomUsers();
  },

  methods: {
    getRandomUsers: function () {
      axios
        .get("api-users/get-random-users/", {
          headers: {
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          if (res.data["random_users"]) {
            this.users = res.data["random_users"];
          }
        });
    },
  },
};
</script>