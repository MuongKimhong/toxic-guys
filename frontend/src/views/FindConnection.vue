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
              <tr v-for="item in desserts" :key="item.name">
                <td>{{ item.name }}</td>
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
    desserts: [
      {
        name: "Frozen Yogurt",
        calories: 159,
      },
      {
        name: "Ice cream sandwich",
        calories: 237,
      },
      {
        name: "Eclair",
        calories: 262,
      },
      {
        name: "Cupcake",
        calories: 305,
      },
      {
        name: "Gingerbread",
        calories: 356,
      },
      {
        name: "Jelly bean",
        calories: 375,
      },
      {
        name: "Lollipop",
        calories: 392,
      },
      {
        name: "Honeycomb",
        calories: 408,
      },
      {
        name: "Donut",
        calories: 452,
      },
      {
        name: "KitKat",
        calories: 518,
      },
      {
        name: "KitKat",
        calories: 518,
      },
    ],
  }),

  methods: {},
};
</script>