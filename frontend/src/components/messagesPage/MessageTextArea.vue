<template>
  <v-card-text
    class="white--text py-2 px-2 d-flex flex-column"
    style="background-color: rgb(78, 78, 78); height: 100%; overflow-y: auto"
    id="message-text-area"
  >
    <v-spacer></v-spacer>
    <div v-for="(message, index) in messages" :key="index" class="text my-1">
      <div v-if="message.sender.id != $store.state.user.id">
        <v-avatar size="28" color="white" style="float: left">
          <v-img
            v-if="message.sender.profile_url == ''"
            :src="require(`../../../public/userimg.png`)"
          ></v-img>
          <v-img v-else :src="message.sender.profile_url"></v-img>
        </v-avatar>
        <div
          v-if="message.images.length > 0"
          class="d-flex"
          style="width: 200px; height: 60px"
        >
          <v-img
            :width="50"
            v-for="(image, i) in message.images"
            :key="i"
            :src="image.image"
          ></v-img>
        </div>
        <span v-if="message.text != ''" class="message-text-left">
          {{ message.text }}
        </span>
      </div>
      <div v-else>
        <span v-if="message.text != ''" class="message-text-right">{{
          message.text
        }}</span>
      </div>
    </div>
    <div class="text" style=""></div>
  </v-card-text>
</template>

<script>
export default {
  name: "MessageTextArea",
  props: ["messages"],

  created() {
    this.scrollToBottom(100);
  },

  watch: {
    messages(newValue) {
      if (newValue) {
        this.scrollToBottom(50);
      }
    },
  },

  methods: {
    scrollToBottom: function (timeout) {
      setTimeout(() => {
        var element = document.getElementById("message-text-area");
        document.getElementById("message-text-area").scrollTop =
          element.scrollHeight;
      }, timeout);
    },
  },
};
</script>

<style scoped>
.message-text-left {
  border-radius: 16px;
  padding-top: 3px;
  padding-bottom: 3px;
  padding-left: 10px;
  padding-right: 10px;
  background-color: black;
  font-size: 12px;
  float: left;
  margin-left: 5px;
}
.message-text-right {
  border-radius: 16px;
  padding-top: 3px;
  padding-bottom: 3px;
  padding-left: 10px;
  padding-right: 10px;
  background-color: black;
  font-size: 12px;
  float: right;
}
</style>