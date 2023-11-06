<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="8" class="ml-auto mr-auto">
        <div v-if="group != null" class="text-center"></div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "GroupDetail",

  data: () => ({
    group: null,
  }),

  created() {
    this.getGroupDetail();
  },

  methods: {
    getGroupDetail: function () {
      axios
        .get("api-groups/group-detail/", {
          params: {
            room_id: this.$route.params.chatroomId,
          },
          headers: {
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          if (res.data["group"]) {
            this.group = res.data["group"];
          }
        })
        .catch((err) => {
          if (err.response.data["group_err"]) return;
          else if (err.response.data["user_err"]) return;
          else if (err.response.data["not_in_group"]) return;
        });
    },
  },
};
</script>