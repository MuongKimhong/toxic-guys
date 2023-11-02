<template>
  <v-card-text
    class="white--text py-2 px-2 d-flex flex-column"
    style="background-color: rgb(78, 78, 78); height: 100%"
  >
    <v-spacer></v-spacer>
    <div v-for="(message, index) in messages" :key="index" class="text my-2">
      <div v-if="message.sender.id != $store.state.user.id">
        <v-avatar size="28" color="white" style="float: left">
          <v-img
            v-if="message.sender.profile_url == ''"
            :src="require(`../../../public/userimg.png`)"
          ></v-img>
          <v-img v-else :src="message.sender.profile_url"></v-img>
        </v-avatar>
        <span class="message-text-left">{{ message.text }}</span>
      </div>
      <div v-else>
        <span class="message-text-right">{{ message.text }}</span>
      </div>
    </div>
    <div class="text" style=""></div>
  </v-card-text>
</template>

<script>
export default {
  name: "MessageTextArea",
  props: ["messages"],
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