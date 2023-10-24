<template>
  <v-container>
    <v-row>
      <v-col cols="8" class="mr-auto ml-auto">
        <v-text-field
          class="mt-2"
          rounded
          dense
          label="Search users"
          dark
          outlined
          append-icon="mdi-account-search"
          v-model="searchText"
          @keyup="typingEvent()"
        ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "SearchUser",

  data: () => ({
    searchText: "",
  }),

  methods: {
    typingEvent: function () {
      this.$emit("userTyping", this.searchText);
    },
  },
};
</script>