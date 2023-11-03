<template>
  <v-navigation-drawer
    permanent
    style="background-color: rgb(95, 95, 95); height: 800px"
    class="navigation-drawer"
  >
    <v-list density="compact" nav>
      <v-list-item
        v-for="(chatroom, index) in chatrooms"
        :key="index"
        class="user-list pb-1"
        @click="chatroomOnClick(chatroom)"
      >
        <div v-if="chatroom.type == 'user'">
          <div v-if="chatroom.creator.id != $store.state.user.id">
            <v-avatar
              v-if="chatroom.creator.profile_url == ''"
              size="36"
              color="white"
            >
              <v-img :src="require(`../../../public/userimg.png`)"></v-img>
            </v-avatar>
            <v-avatar v-else size="36" color="white">
              <v-img :src="chatroom.creator.profile_url"></v-img>
            </v-avatar>
            <span class="white--text ml-2">
              {{ chatroom.creator.username }}
            </span>
          </div>
          <div v-else-if="chatroom.member.id != $store.state.user.id">
            <v-avatar
              v-if="chatroom.creator.profile_url == ''"
              size="36"
              color="white"
            >
              <v-img :src="require(`../../../public/userimg.png`)"></v-img>
            </v-avatar>
            <v-avatar v-else size="36" color="white">
              <v-img :src="chatroom.creator.profile_url"></v-img>
            </v-avatar>
            <span class="white--text ml-2">{{ chatroom.member.username }}</span>
          </div>
        </div>
        <div v-if="chatroom.type == 'group'">
          <div>
            <v-avatar size="36" color="white">
              <v-img
                v-if="chatroom.group.profile == ''"
                :src="require(`../../../public/groupimg.png`)"
              ></v-img>
              <v-img v-else :src="chatroom.group.profile"></v-img>
            </v-avatar>
            <span class="white--text ml-2">
              {{ chatroom.group.name }}
            </span>
          </div>
        </div>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import axios from "axios";

export default {
  name: "UserListInMessagePage",

  data: () => ({
    chatrooms: [],
  }),

  created() {
    this.getChatRoomList();
  },

  methods: {
    getChatRoomList: function () {
      axios
        .get("api-chats/get-chatroom-list/", {
          headers: {
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          this.chatrooms = res.data["chatrooms"];
          if (this.chatrooms.length > 0) {
            this.$emit("chatroomOnClick", this.chatrooms[0]);
          }
          console.log(this.chatrooms);
        });
    },

    chatroomOnClick: function (chatroomObject) {
      this.$emit("chatroomOnClick", chatroomObject);
    },
  },
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