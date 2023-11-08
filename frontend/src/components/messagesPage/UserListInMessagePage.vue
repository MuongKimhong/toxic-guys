<template>
  <v-navigation-drawer
    permanent
    style="background-color: rgb(95, 95, 95); height: 800px"
    class="navigation-drawer"
  >
    <v-list nav>
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
            <span class="white--text ml-2" style="font-size: 13px">
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
          <small
            v-if="chatroom.last_message_text != ''"
            class="white--text ml-1"
          >
            {{ chatroom.last_message_text }}
          </small>
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
            <span class="white--text ml-2" style="font-size: 13px">
              {{ chatroom.group.name }}
            </span>
          </div>
          <small
            v-if="chatroom.last_message_text != ''"
            class="white--text ml-1"
          >
            {{ chatroom.last_message_sender_name }} :
            {{ chatroom.last_message_text }}
          </small>
        </div>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "UserListInMessagePage",

  props: ["chatrooms"],

  methods: {
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