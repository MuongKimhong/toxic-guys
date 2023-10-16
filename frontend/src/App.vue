<template>
  <v-app>
    <Navbar />

    <v-main class="pageColor">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Navbar from "../src/components/Navbar.vue";

export default {
  name: "App",

  components: {
    Navbar,
  },

  data: () => ({
    //
  }),
};
</script>

<style>
.pageColor {
  background-color: rgb(78, 78, 78);
  min-height: 100%;
  color: white;
}
</style>