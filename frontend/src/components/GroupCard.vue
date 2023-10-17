<template>
  <v-col cols="3">
    <v-card flat dense class="text-center py-5 px-2 group-card">
      <v-avatar style="background-color: grey" size="120">
        <i class="fas fa-users white--text" style="font-size: 50px"></i>
      </v-avatar>

      <h3 class="text-center mt-2 white--text">Group Name</h3>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "GroupCard",
};
</script>

<style scoped>
.group-card {
  background-color: rgb(78, 78, 78);
  cursor: pointer;
}
.group-card:hover {
  background-color: rgb(82, 82, 82);
}
</style>