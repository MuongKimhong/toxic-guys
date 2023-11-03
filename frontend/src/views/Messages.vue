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
                <UserDetailNavbar :chatroom="selectedChatRoom" />
                <MessageTextArea :messages="messagesInChatroom" />
                <v-spacer></v-spacer>

                <v-card-actions style="background-color: rgb(78, 78, 78)">
                  <span class="mr-2">
                    <i
                      class="fas fa-images white--text"
                      id="images-icon"
                      style="font-size: 20px"
                    ></i>
                  </span>
                  <v-text-field
                    rounded
                    outlined
                    dense
                    label="Write message here"
                    dark
                    hide-details
                    v-model="messageText"
                    append-icon="mdi-arrow-up"
                    @click:append="sendMessage()"
                  ></v-text-field>
                </v-card-actions>
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
import axios from "axios";

export default {
  name: "Messages",

  components: {
    UserListInMessagePage,
    UserDetailNavbar,
    MessageTextArea,
  },

  data: () => ({
    selectedChatRoom: null,

    messagesInChatroom: [],
    messageText: "",
  }),

  created() {
    document.addEventListener("keyup", (event) => {
      if (event.key == "Enter") {
        if (this.messageText.trim() != "") {
          this.sendMessage();
        }
      }
    });
  },

  methods: {
    sendMessageIconClick: function () {},

    chatroomOnClick: function (chatroomObject) {
      this.selectedChatRoom = chatroomObject;
      this.getMessagesInChatroom(chatroomObject);
    },

    getMessagesInChatroom: function (chatroomObject) {
      if (chatroomObject.type === "user") {
        axios
          .get("api-chats/get-messages-in-chatroom/", {
            params: {
              chatroom_id: chatroomObject.id,
            },
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          })
          .then((res) => {
            this.messagesInChatroom = res.data["messages"];
          });
      } else if (chatroomObject.type === "group") {
        axios
          .get("api-chats/get-messages-in-group-chatroom/", {
            params: {
              group_chatroom_id: chatroomObject.id,
            },
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          })
          .then((res) => {
            this.messagesInChatroom = res.data["messages"];
          });
      }
    },

    sendMessage: function () {
      if (this.messageText.trim() === "") return;

      var receiverId = null;

      if (this.selectedChatRoom.creator.id == this.$store.state.user.id) {
        receiverId = this.selectedChatRoom.member.id;
      } else {
        receiverId = this.selectedChatRoom.creator.id;
      }

      axios
        .post(
          "api-chats/send-message/",
          {
            chatroom_id: this.selectedChatRoom.id,
            text: this.messageText,
            receiver_id: receiverId,
          },
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          }
        )
        .then((res) => {
          this.messageText = "";
          console.log(res.data["message"]);
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
#images-icon {
  cursor: pointer;
}
</style>