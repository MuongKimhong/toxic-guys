<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="12" class="mr-auto ml-auto">
        <div class="text-right mt-2">
          <v-btn
            small
            class="mr-4 green text-capitalize white--text"
            @click="$router.push({ name: 'CreateNewGroup' }).catch(() => {})"
          >
            New group
          </v-btn>
          <v-btn
            small
            class="green text-capitalize white--text"
            @click="$router.push({ name: 'FindConnection' })"
          >
            New connection
          </v-btn>
        </div>
        <div class="mt-5">
          <v-card class="px-0 py-0 white--text message-card d-flex">
            <v-layout>
              <UserListInMessagePage @chatroomOnClick="chatroomOnClick" />
              <v-card class="d-flex flex-column message-area">
                <UserDetailNavbar />
                <MessageTextArea :messages="messagesInChatroom" />
                <v-spacer></v-spacer>
                <SendTextArea />
              </v-card>
            </v-layout>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import UserListInMessagePage from "../components/messagesPage/UserListInMessagePage.vue";
import UserDetailNavbar from "../components/messagesPage/UserDetailNavbar.vue";
import MessageTextArea from "../components/messagesPage/MessageTextArea.vue";
import SendTextArea from "../components/messagesPage/SendTextArea.vue";
import axios from "axios";

export default {
  name: "Messages",

  components: {
    UserListInMessagePage,
    UserDetailNavbar,
    MessageTextArea,
    SendTextArea,
  },

  data: () => ({
    selectedChatRoomId: null,

    messagesInChatroom: [],
  }),

  methods: {
    sendMessageIconClick: function () {},

    chatroomOnClick: function (chatroomId) {
      this.selectedChatRoomId = chatroomId;
      this.getMessagesInChatroom(chatroomId);
    },

    getMessagesInChatroom: function (chatroomId) {
      axios
        .get("api-chats/get-messages-in-chatroom/", {
          params: {
            chatroom_id: chatroomId,
          },
          headers: {
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          this.messagesInChatroom = res.data["messages"];
        });
    },
  },
};
</script>

<style scoped>
.message-card {
  background-color: rgb(95, 95, 95);
  border-radius: 5px;
  height: 800px;
}
.message-area {
  background-color: rgb(78, 78, 78);
  width: 100%;
  border-radius: 0;
  padding: 5px;
}
</style>