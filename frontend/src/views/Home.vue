<template>
  <v-container>
    <!-- not signed in -->
    <div v-if="$store.state.user.accessToken == null">
      <div class="mt-10">
        <SearchUser />

        <hr
          style="
            height: 1px;
            background-color: grey;
            border: none;
            margin-top: 50px;
            margin-bottom: 50px;
          "
        />

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
};
</script>

<style scoped>
</style>