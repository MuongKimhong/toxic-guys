<template>
  <v-container>
    <!-- not signed in -->
    <div v-if="$store.state.user.accessToken == null">
      <div class="mt-10">
        <SearchUser :showText="true" @userTyping="searchUsersAcceptAnonymousMessage"/>

        <hr class="hr-element" />

        <div>
          <h1 class="text-center mb-5">Explore public groups</h1>
          <v-row justify="space-around">
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
          </v-row>
        </div>
      </div>
    </div>

    <!-- signed in -->
    <div v-else>
      <div class="mt-10">
        <h1 class="text-center mb-5">Public groups</h1>
        <v-row justify="space-around">
          <GroupCard />
          <GroupCard />
          <GroupCard />
          <GroupCard />
        </v-row>
      </div>

      <hr class="hr-element" />

      <div class="mt-10">
        <h1 class="text-center mb-5">Your groups</h1>
        <v-row justify="space-around">
          <GroupCard />
          <GroupCard />
          <GroupCard />
          <GroupCard />
          <GroupCard />
        </v-row>
      </div>
    </div>
  </v-container>
</template>

<script>
import SearchUser from "../components/SearchUser.vue";
import GroupCard from "../components/GroupCard.vue";

export default {
  name: "Home",

  components: {
    SearchUser,
    GroupCard,
  },

  methods: {
    searchUsersAcceptAnonymousMessage: function (searchText) {
    }
  }
};
</script>

<style scoped>
.hr-element {
  background-color: grey;
  height: 1px;
  border: none;
  margin-top: 50px;
  margin-bottom: 50px;
}
</style>
