<template>
  <v-navigation-drawer
    permanent
    style="background-color: rgb(95, 95, 95); height: 800px"
    class="navigation-drawer"
  >
    <v-list density="compact" nav>
      <v-list-item v-for="(i, index) in 12" :key="index" class="user-list pb-1">
        <v-avatar size="36" color="white"></v-avatar>
        <span class="white--text ml-2">Richard </span>
      </v-list-item>
      <v-list-item class="user-list pb-1">
        <v-avatar size="36" color="white"></v-avatar>
        <span class="white--text ml-2">Richard</span>
      </v-list-item>
      <v-list-item class="user-list pb-1">
        <v-avatar size="36" color="white"></v-avatar>
        <span class="white--text ml-2">Richard </span>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "UserListInMessagePage",
};
</script>

<style scoped>
.user-list {
  border-bottom: solid;
  border-bottom-width: 1px;
  border-bottom-color: grey;
  cursor: pointer;
  font-size: 14px;
}
.user-list:hover {
  background-color: rgb(100, 100, 100);
}
</style>