<template>
  <v-card-text
    class="white--text py-2 px-2 d-flex flex-column"
    style="background-color: rgb(78, 78, 78); height: 100%"
  >
    <v-spacer></v-spacer>
    <div class="text my-2">
      <v-avatar size="28" color="white" style="float: left"></v-avatar>
      <span class="message-text-left">Hey man</span>
    </div>
    <div class="text" style="">
      <span class="message-text-right"> Yo what's up </span>
    </div>
  </v-card-text>
</template>

<script>
export default {
  name: "MessageTextArea",
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