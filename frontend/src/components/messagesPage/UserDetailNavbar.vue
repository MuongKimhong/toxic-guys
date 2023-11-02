<template>
  <v-card-title
    style="background-color: rgb(95, 95, 95); border-radius: 10px; padding: 5px"
  >
    <v-avatar
      v-if="chatroom.creator.id == $store.state.user.id"
      size="28"
      color="white"
      class="ml-2"
    >
      <v-img
        v-if="chatroom.member.profile_url == ''"
        :src="require(`../../../public/userimg.png`)"
      ></v-img>
      <v-img v-else :src="chatroom.member.profile_url"></v-img>
    </v-avatar>
    <v-avatar v-else size="28" color="white" class="ml-2">
      <v-img
        v-if="chatroom.creator.profile_url == ''"
        :src="require(`../../../public/userimg.png`)"
      ></v-img>
      <v-img v-else :src="chatroom.creator.profile_url"></v-img>
    </v-avatar>

    <span
      v-if="chatroom.creator.id == $store.state.user.id"
      class="white--text ml-2"
      style="font-size: 16px"
    >
      {{ chatroom.member.username }}
    </span>
    <span v-else class="white--text ml-2" style="font-size: 16px">
      {{ chatroom.creator.username }}
    </span>
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
  props: ["chatroom"],
};
</script>