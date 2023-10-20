<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="12" class="mr-auto ml-auto">
        <div class="text-right mt-2">
          <v-btn small class="mr-4 green text-capitalize white--text">
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
              <UserListInMessagePage />
              <v-card class="d-flex flex-column message-area">
                <UserDetailNavbar />
                <MessageTextArea />
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

export default {
  name: "Messages",
  components: {
    UserListInMessagePage,
    UserDetailNavbar,
    MessageTextArea,
    SendTextArea,
  },
  methods: {
    sendMessageIconClick: function () {},
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