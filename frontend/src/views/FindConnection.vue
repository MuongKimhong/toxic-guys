<template>
  <v-container>
    <SearchUser />

    <div class="mt-5">
      <v-card
        style="background-color: rgb(95, 95, 95); height: 600px"
        class="white--text"
      >
        <v-simple-table
          style="height: 600px; background-color: rgb(95, 95, 95)"
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
                <td>{{ item.username }}</td>
                <td class="text-right">
                  <v-btn small class="dark-grey white--text text-capitalize"
                    >Connect</v-btn
                  >
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
import SearchUser from "../components/SearchUser.vue";

export default {
  name: "FindConnection",

  components: {
    SearchUser,
  },

  data: () => ({
    users: [],
  }),

  methods: {},
};
</script>