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
              <UserListInMessagePage
                @chatroomOnClick="chatroomOnClick"
                :chatrooms="chatrooms"
              />
              <v-card class="d-flex flex-column message-area">
                <UserDetailNavbar :chatroom="selectedChatRoom" />
                <MessageTextArea :messages="messagesInChatroom" />
                <v-spacer></v-spacer>

                <!-- select images to upload -->
                <v-row v-if="selectedImages.length > 0">
                  <v-col
                    v-for="n in 3"
                    :key="n"
                    class="d-flex child-flex"
                    cols="1"
                  >
                    <v-img
                      :src="`https://picsum.photos/500/300?image=${n * 5 + 10}`"
                      :lazy-src="`https://picsum.photos/10/6?image=${
                        n * 5 + 10
                      }`"
                      aspect-ratio="1"
                      cover
                      class="bg-grey-lighten-2"
                    >
                    </v-img>
                  </v-col>
                </v-row>

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
    chatrooms: [],
    selectedChatRoom: null,

    messagesInChatroom: [],
    messageText: "",

    selectedImages: []
  }),

  created() {
    document.addEventListener("keyup", (event) => {
      if (event.key == "Enter") {
        if (this.messageText.trim() != "") {
          this.sendMessage();
        }
      }
    });

    this.getChatRoomList();
    this.listenToWebSocketEventHandling();
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
      if (this.selectedChatRoom.type === "user") {
        this.sendMessageForChatRoom();
      } else if (this.selectedChatRoom.type === "group") {
        this.sendMessageForGroupChatRoom();
      }
    },

    reorderChatRooms: function (type, lastMessage) {
      for (const index in this.chatrooms) {
        if (this.chatrooms[index].type === type) {
          if (this.selectedChatRoom.id === this.chatrooms[index].id) {
            this.chatrooms.splice(index, 1);
            this.chatrooms.unshift(this.selectedChatRoom);
            this.chatrooms[0]["last_message_text"] = lastMessage.text;
            this.chatrooms[0]["last_message_sender_name"] = lastMessage.sender.username;
            break;
          }
        }
      }
    },

    reorderChatRoomsWithoutSelectChatroom: function (type, firstChatroom, lastMessage) {
      for (const i in this.chatrooms) {
        if (this.chatrooms[i].type === type) {
          if (this.chatrooms[i].id === firstChatroom.id) {
            this.chatrooms.splice(i, 1);
            this.chatrooms.unshift(firstChatroom);
            this.chatrooms[0]["last_message_text"] = lastMessage.text;
            this.chatrooms[0]["last_message_sender_name"] = lastMessage.sender.username;
            break;
          }
        }
      }
    },

    sendMessageForChatRoom: function () {
      if (this.messageText.trim() === "") return;

      var receiverId = null;

      if (this.selectedChatRoom.creator.id == this.$store.state.user.id) {
        receiverId = this.selectedChatRoom.member.id;
      } 
      else {
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
          this.messagesInChatroom.push(res.data["message"]);
          this.reorderChatRooms("user", res.data["message"]);

          for (const i in this.chatrooms) {
            if (this.chatrooms[i].type == "user") {
              if (this.chatrooms[i].id === this.selectedChatRoom.id) {
                this.chatrooms[i]["last_message_text"] = res.data["message"].text;
                this.chatrooms[i]["last_message_sender_name"] = res.data["message"].sender.username;
                break;
              }
            }
          }

          var webSocketData = {
            chatroomId: this.selectedChatRoom.id,
            message: res.data["message"]
          };
          this.$webSocket.emit("send-message", JSON.stringify(webSocketData));
        });
    },

    sendMessageForGroupChatRoom: function () {
      if (this.messageText.trim() === "") return;

      axios
        .post(
          "api-chats/send-message-for-group-chatroom/",
          {
            chatroom_id: this.selectedChatRoom.id,
            text: this.messageText,
          },
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          })
        .then((res) => {
          this.messageText = "";
          this.messagesInChatroom.push(res.data["message"]);
          this.reorderChatRooms("group", res.data["message"]);

          for (const i in this.chatrooms) {
            if (this.chatrooms[i].type == "group") {
              if (this.chatrooms[i].id === this.selectedChatRoom.id) {
                this.chatrooms[i]["last_message_text"] = res.data["message"].text;
                this.chatrooms[i]["last_message_sender_name"] = res.data["message"].sender.username;
                break;
              }
            }
          }

          var webSocketData = {
            groupChatroomId: this.selectedChatRoom.id,
            message: res.data["message"],
          };
          this.$webSocket.emit("send-message-group", JSON.stringify(webSocketData));
        });
    },

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
            this.selectedChatRoom = this.chatrooms[0];
            this.getMessagesInChatroom(this.selectedChatRoom);
          }
        });
    },

    updateMessagesOnWebSocketEvent: function (chatroomType, messageData) {
      var roomIdKeyWord = "";

      if (chatroomType === "user") roomIdKeyWord = "chatroomId";
      else roomIdKeyWord = "groupChatroomId";

      for (const i in this.chatrooms) {
        if (this.chatrooms[i].type === chatroomType) {
          if (this.chatrooms[i].id === messageData[`${roomIdKeyWord}`]) {
            if (this.selectedChatRoom.type === chatroomType) {
              if (this.selectedChatRoom.id === messageData[`${roomIdKeyWord}`]) {
                if (messageData.message.sender.id != this.$store.state.user.id) {
                  this.messagesInChatroom.push(messageData.message);
                  this.chatrooms[i]["last_message_text"] = messageData.message.text;
                  this.chatrooms[i]["last_message_sender_name"] = messageData.message.sender.username;
                }
              }
              else {
                this.reorderChatRoomsWithoutSelectChatroom(chatroomType, this.chatrooms[i], messageData.message);
              }
            }
            else {
              this.reorderChatRoomsWithoutSelectChatroom(chatroomType, this.chatrooms[i], messageData.message);
            }
          }
        }
      }
    },

    listenToWebSocketEventHandling: function () {
      this.$webSocket.on("new-message", (message) => {
        this.updateMessagesOnWebSocketEvent("user", JSON.parse(message));
      });

      this.$webSocket.on("group-new-message", (data) => {
        this.updateMessagesOnWebSocketEvent("group", JSON.parse(data));
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