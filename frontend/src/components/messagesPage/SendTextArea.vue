<template>
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
      append-icon="mdi-arrow-up"
      @click:append="sendMessageIconClick()"
    ></v-text-field>
  </v-card-actions>
</template>

<script>
export default {
  name: "SendTextArea",
};
</script>

<style scoped>
#images-icon {
  cursor: pointer;
}
</style>