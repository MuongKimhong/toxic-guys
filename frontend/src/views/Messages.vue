<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="12" class="mr-auto ml-auto">
        <div>
          <v-card class="px-0 py-0 white--text message-card d-flex">
            <v-layout>
              <UserListInMessagePage />
              <v-card
                class="d-flex flex-column"
                style="
                  background-color: white;
                  width: 100%;
                  border-radius: 0;
                  padding: 5px;
                "
              >
                <v-card-title>kasj</v-card-title>
                <v-card-text>;lkasjdf</v-card-text>
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
import SendTextArea from "../components/messagesPage/SendTextArea.vue";

export default {
  name: "Messages",
  components: {
    UserListInMessagePage,
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
</style>