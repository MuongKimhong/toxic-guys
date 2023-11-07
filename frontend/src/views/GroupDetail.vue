<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="8" class="ml-auto mr-auto">
        <div v-if="group != null" class="text-center">
          <div class="text-center">
            <v-avatar
              v-if="newGroupImageUrl === null"
              size="120"
              color="white"
              class="ml-auto mr-auto"
            >
              <v-img
                v-if="group.group.profile === ''"
                :src="require(`../../public/groupimg.png`)"
              ></v-img>
              <v-img v-else :src="group.group.profile"></v-img>
            </v-avatar>
            <v-avatar v-else size="120" color="white" class="ml-auto mr-auto">
              <v-img :src="newGroupImageUrl"></v-img>
            </v-avatar>

            <div class="text-center mt-5">
              <v-btn
                small
                class="text-capitalize white--text"
                style="background-color: rgb(95, 95, 95)"
                @click="changeImageBtnOnClick()"
              >
                change Image
              </v-btn>
            </div>
          </div>

          <div class="mt-10">
            <v-text-field
              dark
              label="Group name"
              dense
              outlined
              rounded
              counter="20"
              v-model="groupName"
              :error-messages="err.name"
              @keyup="groupNameOnChange()"
            ></v-text-field>

            <v-select
              :items="['Public', 'Private']"
              density="compact"
              dense
              label="Group type"
              dark
              outlined
              rounded
              v-model="groupType"
              :error-messages="err.type"
              @change="groupTypeOnChange()"
            ></v-select>

            <v-textarea
              rounded
              outlined
              dark
              label="Description"
              v-model="groupDescription"
              counter="30"
              @keyup="groupDescriptionOnChange()"
            >
            </v-textarea>
          </div>

          <div class="text-right mt-6">
            <v-btn
              class="text-capitalize mr-4"
              small
              @click="$router.push({ name: 'Messages' })"
            >
              Cancel
            </v-btn>
            <v-btn
              v-if="changeDetected === false"
              class="text-capitalize white--text"
              dark
              small
              disabled
            >
              Save
            </v-btn>
            <v-btn
              v-else
              class="text-capitalize white--text"
              dark
              small
              @click="saveBtnOnClick()"
            >
              Save
            </v-btn>
          </div>

          <!-- members -->
          <div class="mt-10">
            <v-simple-table
              style="background-color: rgb(78, 78, 78)"
              dark
              class="white--text"
            >
              <template v-slot:default>
                <thead>
                  <tr>
                    <th class="text-left white--text">Members</th>
                    <th class="text-right white--text">
                      <v-btn
                        x-small
                        class="green text-capitalize white--text"
                        @click="addMemberBtnOnClick()"
                      >
                        Add member
                      </v-btn>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(user, index) in group.members" :key="index">
                    <td class="text-left">
                      <v-avatar size="28" color="white">
                        <v-img
                          v-if="user.profile_url == ''"
                          :src="require('../../public/userimg.png')"
                        ></v-img>
                        <v-img v-else :src="user.profile_url"></v-img>
                      </v-avatar>
                      <span class="ml-2">
                        {{ user.username }}
                        <span v-if="group.group.creator.id === user.id">
                          (admin)
                        </span>
                      </span>
                    </td>
                    <td class="text-right">
                      <v-btn
                        v-if="
                          group.group.creator.id === $store.state.user.id &&
                          user.id != $store.state.user.id
                        "
                        small
                        class="dark-grey white--text text-capitalize"
                      >
                        Kick
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </div>

          <v-dialog v-model="showSearchUserDialog" width="450" height="600">
            <v-card width="450" height="600" class="px-3 py-3" dark>
              <v-text-field
                class="mt-2"
                dense
                label="Search users"
                dark
                outlined
                append-icon="mdi-account-search"
                v-model="searchText"
                @keyup="searchUsersNotInGroup()"
              ></v-text-field>

              <v-simple-table dark class="white--text">
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left white--text">Users</th>
                      <th class="text-right white--text"></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(user, index) in randomUsers" :key="index">
                      <td class="text-left">
                        <v-avatar size="28" color="white">
                          <v-img
                            v-if="user.profile_url == ''"
                            :src="require('../../public/userimg.png')"
                          ></v-img>
                          <v-img v-else :src="user.profile_url"></v-img>
                        </v-avatar>
                        <span class="ml-2">
                          {{ user.username }}
                        </span>
                      </td>
                      <td class="text-right">
                        <v-btn
                          x-small
                          class="white black--text text-capitalize"
                          v-if="user.invited == false"
                          @click="inviteBtnOnClick(user.id, index)"
                        >
                          Invite
                        </v-btn>
                        <v-btn
                          x-small
                          class="white black--text text-capitalize"
                          v-else
                          @click="inviteBtnOnClick(user.id, index)"
                        >
                          Uninvite
                        </v-btn>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>

              <div class="px-2 mt-5 d-flex">
                <v-btn
                  v-if="currentPage > 1 && currentPage <= totalPages"
                  x-small
                  class="text-capitalize mr-1"
                  @click="prevBtnOnClick()"
                >
                  Previous
                </v-btn>
                <v-btn
                  v-if="currentPage >= 1 && currentPage < totalPages"
                  x-small
                  class="text-capitalize ml-1"
                  @click="nextBtnOnClick()"
                >
                  Next >
                </v-btn>
                <v-btn
                  class="ml-auto green white--text text-capitalize"
                  x-small
                  @click="confirmBtnOnClick()"
                >
                  Confirm
                </v-btn>
              </div>
            </v-card>
          </v-dialog>
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

    newGroupImage: null,
    newGroupImageUrl: null,
    groupType: "",
    groupName: "",
    groupDescription: "",

    err: {
      name: "",
      type: "",
      description: "",
    },
    changeDetected: false,

    showSearchUserDialog: false,
    searchText: "",
    randomUsers: [],
    currentPage: 1,
    totalPages: 0,

    invitedUserIds: [],
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
            this.groupName = res.data["group"]["group"]["name"];
            this.groupDescription = res.data["group"]["group"]["description"];

            if (res.data["group"]["group"]["is_public"] === true) {
              this.groupType = "Public";
            } else {
              this.groupType = "Private";
            }
          }
        })
        .catch((err) => {
          if (err.response.data["group_err"]) return;
          else if (err.response.data["user_err"]) return;
          else if (err.response.data["not_in_group"]) return;
        });
    },

    changeImageBtnOnClick: function () {
      let self = this;
      let input = document.createElement("input");
      input.type = "file";
      input.accept = ".jpg,.JPEG,.png";
      input.onchange = () => {
        let files = Array.from(input.files);
        self.newGroupImage = files[0];
        self.newGroupImageUrl = URL.createObjectURL(files[0]);
        input.remove();
        self.changeDetected = true;
      };
      input.click();
    },

    groupNameOnChange: function () {
      if (this.groupName === this.group["group"]["name"])
        this.changeDetected = false;
      else this.changeDetected = true;
    },

    groupDescriptionOnChange: function () {
      if (this.groupDescription === this.group["group"]["description"])
        this.changeDetected = false;
      else this.changeDetected = true;
    },

    groupTypeOnChange: function () {
      if (
        this.group["group"]["is_public"] == true &&
        this.groupType === "Public"
      ) {
        this.changeDetected = false;
      } else if (
        this.group["group"]["is_private"] == true &&
        this.groupType === "Private"
      ) {
        this.changeDetected = false;
      } else {
        this.changeDetected = true;
      }
    },

    saveBtnOnClick: function () {
      if (this.groupName.length > 20) return;
      else if (this.groupDescription.length > 30) return;
      else if (this.groupType != "Public" && this.groupType != "Private")
        return;

      var formData = new FormData();
      formData.append("name", this.groupName);
      formData.append("status", this.groupType);
      formData.append("profile", this.newGroupImage);
      formData.append("description", this.groupDescription);
      formData.append("room_id", this.group["id"]);

      axios
        .post("api-groups/update-group-detail/", formData, {
          headers: {
            "content-type": "multipart/form-data",
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then(() => {
          this.changeDetected = false;
        })
        .catch(() => {});
    },

    getRandomUsersNotInGroup: function () {
      axios
        .get("api-groups/get-users-not-in-group/", {
          params: {
            room_id: this.group.id,
            number_per_page: 8,
            page: this.currentPage,
          },
          headers: {
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          this.randomUsers = res.data["random_users"];
          this.totalPages = res.data["total_pages"];

          if (this.invitedUserIds.length > 0) {
            for (const i in this.randomUsers) {
              if (
                this.invitedUserIds.includes(this.randomUsers[i]["id"]) === true
              ) {
                this.randomUsers[i]["invited"] = true;
              }
            }
          }
        });
    },

    addMemberBtnOnClick: function () {
      this.getRandomUsersNotInGroup();
      this.showSearchUserDialog = true;
    },

    nextBtnOnClick: function () {
      this.currentPage = this.currentPage + 1;
      this.getRandomUsersNotInGroup();
    },

    prevBtnOnClick: function () {
      this.currentPage = this.currentPage - 1;
      this.getRandomUsersNotInGroup();
    },

    inviteBtnOnClick: function (userId, index) {
      this.randomUsers[index]["invited"] = !this.randomUsers[index]["invited"];

      if (this.invitedUserIds.includes(userId) === false) {
        this.invitedUserIds.push(userId);
      } else {
        for (const i in this.invitedUserIds) {
          if (this.invitedUserIds[i] === userId) {
            this.invitedUserIds.splice(i, 1);
          }
        }
      }
    },

    confirmBtnOnClick: function () {
      if (this.invitedUserIds.length == 0) return;

      var formData = new FormData();
      formData.append("invited_user_ids", JSON.stringify(this.invitedUserIds));
      formData.append("group", this.group.group.id);

      axios
        .post("api-groups/invite-user-to-join-group/", formData, {
          headers: {
            "content-type": "multipart/form-data",
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          if (res.data["invitation_sent"]) {
            this.$webSocket.emit(
              "group_invitation",
              JSON.stringify(this.invitedUserIds)
            );
            this.randomUsers = [];
            this.showSearchUserDialog = false;
            this.currentPage = 1;
            this.totalPages = 0;
            this.invitedUserIds = [];
          }
        })
        .catch(() => {});
    },

    searchUsersNotInGroup: function () {
      if (this.searchText.trim() === "") this.getRandomUsersNotInGroup();
      else {
        axios
          .get("api-groups/search-users-not-in-group/", {
            params: {
              room_id: this.group.id,
              number_per_page: 8,
              page: this.currentPage,
              search_text: this.searchText,
            },
            headers: {
              Authorization: `Bearer ${this.$store.state.user.accessToken}`,
            },
          })
          .then((res) => {
            if (res.data["users"]) {
              this.randomUsers = res.data["users"];
              this.totalPages = res.data["total_pages"];

              if (this.invitedUserIds.length > 0) {
                for (const i in this.randomUsers) {
                  if (
                    this.invitedUserIds.includes(this.randomUsers[i]["id"]) ===
                    true
                  ) {
                    this.randomUsers[i]["invited"] = true;
                  }
                }
              }
            }
          })
          .catch(() => {});
      }
    },
  },
};
</script>