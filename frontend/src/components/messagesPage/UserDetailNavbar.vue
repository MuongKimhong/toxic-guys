<template>
  <v-card-title
    style="background-color: rgb(95, 95, 95); border-radius: 10px; padding: 5px"
    v-if="chatroom"
  >
    <span v-if="chatroom.type == 'user'">
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
    </span>

    <span v-else>
      <v-avatar size="28" color="white" class="ml-2">
        <v-img
          v-if="chatroom.group.profile == ''"
          :src="require(`../../../public/groupimg.png`)"
        ></v-img>
        <v-img v-else :src="chatroom.group.profile"></v-img>
      </v-avatar>
      <span class="white--text ml-2" style="font-size: 16px">
        {{ chatroom.group.name }}
      </span>
    </span>

    <v-spacer></v-spacer>
    <v-btn small text>
      <span>
        <i class="fas fa-phone white--text" style="font-size: 15px"></i>
      </span>
    </v-btn>
    <v-btn small text @click="threeDotBtnOnClick()">
      <span>
        <i class="fas fa-ellipsis-h white--text" style="font-size: 15px"></i>
      </span>
    </v-btn>

    <v-dialog v-model="showGroupThreeDotDialog" width="600" height="600">
      <v-card width="600" height="600" class="px-5 py-5 white--text" dark>
        <v-text-field
          class="mt-2"
          dense
          label="Search users"
          dark
          outlined
          append-icon="mdi-account-search"
          v-model="searchText"
          @keyup="typingEvent()"
        ></v-text-field>
      </v-card>
    </v-dialog>
  </v-card-title>
</template>

<script>
// import axios from "axios";

export default {
  name: "UserDetailNavbar",
  props: ["chatroom"],

  data: () => ({
    showGroupThreeDotDialog: true,
    randomUsers: [],
  }),

  methods: {
    threeDotBtnOnClick: function () {
      // if (chatroom.type === "group") {
      // }
    },

    typingEvent: function () {},

    getRandomUsers: function () {},
  },
};
</script>