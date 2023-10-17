<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="12" class="mr-auto ml-auto">
        <div>
          <v-card class="px-0 py-0 white--text message-card">
            <UserListInMessagePage />
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import UserListInMessagePage from "../components/UserListInMessagePage.vue";

export default {
  name: "Messages",
  components: {
    UserListInMessagePage,
  },
};
</script>

<style scoped>
.message-card {
  background-color: rgb(95, 95, 95);
  border-radius: 5px;
  height: 800px;
}
</style>