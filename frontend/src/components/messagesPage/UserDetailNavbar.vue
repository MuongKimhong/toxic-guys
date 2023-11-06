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
    <v-btn small text @click="groupDialog.showDialog = true">
      <span>
        <i class="fas fa-ellipsis-h white--text" style="font-size: 15px"></i>
      </span>
    </v-btn>

    <v-dialog
      v-model="groupDialog.showDialog"
      :width="groupDialog.w"
      :height="groupDialog.h"
    >
      <v-card
        :width="groupDialog.w"
        :height="groupDialog.h"
        class="px-2 py-2 white--text"
        dark
      >
        <v-list>
          <v-list-item class="list-item">
            <span class="ml-auto mr-auto">Group Detail</span>
          </v-list-item>
          <v-list-item v-if="chatroom.type == 'group'">
            <span class="ml-auto mr-auto">Code: {{ chatroom.group.code }}</span>
          </v-list-item>
          <v-list-item>
            <v-btn
              class="ml-auto mr-auto text-capitalize red white--text"
              small
            >
              Leave
            </v-btn>
          </v-list-item>
        </v-list>
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
    groupDialog: {
      w: 200,
      h: 190,
      showDialog: false,
    },

    randomUsers: [],
  }),

  methods: {
    typingEvent: function () {},

    getRandomUsers: function () {},
  },
};
</script>

<style scoped>
.list-item {
  cursor: pointer;
}
.list-item:hover {
  background-color: rgb(95, 95, 95);
}
</style>