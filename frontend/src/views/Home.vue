<template>
  <v-container>
    <!-- not signed in -->
    <div v-if="$store.state.user.accessToken == null">
      <div class="mt-10">
        <SearchUser />
      </div>
    </div>
  </v-container>
</template>

<script>
import SearchUser from "../components/SearchUser.vue";

export default {
  name: "Home",

  components: {
    SearchUser,
  },
};
</script>

<style scoped>
</style>