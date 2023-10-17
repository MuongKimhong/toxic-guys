<template>
  <v-card-title
    style="background-color: rgb(95, 95, 95); border-radius: 10px; padding: 5px"
  >
    <v-avatar size="28" color="white" class="ml-2"></v-avatar>
    <span class="white--text ml-2" style="font-size: 16px">Richard </span>
    <v-spacer></v-spacer>
    <v-btn small text>
      <span>
        <i class="fas fa-phone white--text" style="font-size: 15px"></i>
      </span>
    </v-btn>
    <v-btn small text>
      <span>
        <i class="fas fa-ellipsis-h white--text" style="font-size: 15px"></i>
      </span>
    </v-btn>
  </v-card-title>
</template>

<script>
export default {
  name: "UserDetailNavbar",
};
</script>