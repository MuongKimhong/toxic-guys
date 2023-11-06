<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="8" class="ml-auto mr-auto">
        <div v-if="group != null" class="text-center">
          <div>
            <v-avatar size="160" color="white" class="ml-auto mr-auto">
              <v-img
                v-if="group.group.profile == ''"
                :src="require(`../../public/groupimg.png`)"
              ></v-img>
              <v-img v-else :src="group.group.profile"></v-img>
            </v-avatar>
            <!-- <div class="mt-5">
              <v-btn
                v-if="newProfile === null"
                class="text-capitalize white--text"
                style="background-color: rgb(95, 95, 95)"
                small
                @click="changeProfileBtnOnClick()"
              >
                Change profile
              </v-btn>
              <v-btn
                v-else
                class="text-capitalize white--text"
                style="background-color: green"
                small
                @click="changeProfile()"
              >
                Save image
              </v-btn>
            </div> -->
          </div>

          <v-text-field
            class="my-2"
            dense
            label="Group Name"
            dark
            outlined
            v-model="group.group.name"
            :error-messages="groupNameErr"
          ></v-text-field>
        </div>
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
    copiedGroup: null, // use to check update condition
    groupNameErr: ""
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
            this.copiedGroup = res.data["group"];
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