<template>
  <div>
    <v-app-bar app class="navbar-color" dark height="100">
      <div class="d-flex align-center">
        <h1>ToxicGuys</h1>
      </div>

      <v-spacer></v-spacer>

      <!-- signed in -->
      <div v-if="$store.state.user.accessToken != null">
        <v-btn text>
          <span class="text-capitalize mr-1">Messages</span>
          <i class="fas fa-comments"></i>
        </v-btn>
        <v-btn text>
          <span class="text-capitalize mr-1">Groups</span>
          <i class="fas fa-users"></i>
        </v-btn>
        <v-btn text>
          <span class="text-capitalize mr-1">Anonymous</span>
          <i class="fas fa-question"></i>
        </v-btn>
        <v-btn text>
          <span class="text-capitalize mr-1">Sign Out</span>
          <i class="fas fa-sign-out-alt"></i>
        </v-btn>
      </div>
      <!-- not signed in -->
      <div v-else>
        <v-btn text>
          <span class="text-capitalize">Sign In</span>
        </v-btn>
      </div>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: "Navbar",
};
</script>

<style scoped>
.navbar-color {
  background-color: rgb(95, 95, 95);
  color: white;
}
</style>