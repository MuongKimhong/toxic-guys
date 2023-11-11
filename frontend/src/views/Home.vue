<template>
  <v-container>
    <!-- not signed in -->
    <div v-if="$store.state.user.accessToken == null">
      <div class="mt-10">
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
                id="search-element"
                v-model="searchText"
                @keyup="searchUsersAcceptAnonymousMessageOnTyping()"
              >
              </v-text-field>

              <v-menu
                v-model="showMenu"
                absolute
                :min-width="menuWidth"
                :position-x="menuPositionX"
                :position-y="menuPositionY"
                dark
              >
                <v-list v-if="users.length > 0">
                  <v-list-item
                    v-for="(user, index) in users"
                    :key="index"
                    class="listItem"
                  >
                    <v-list-item-title>
                      <v-avatar size="28" color="white">
                        <v-img
                          v-if="user.profile_url == ''"
                          :src="require(`../../public/userimg.png`)"
                        ></v-img>
                        <v-img v-else :src="user.profile_url"></v-img>
                      </v-avatar>
                      <span class="ml-2">
                        {{ user.username }}
                      </span>
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
                <v-list v-else>
                  <v-list-item>
                    <v-list-item-title>Not found</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>

              <div class="text-center">
                <small class="text-center">
                  Did you know that here you can chat with other people
                  anonymously if they are opened to anonymous conversation?
                </small>
              </div>
            </v-col>
          </v-row>
        </v-container>

        <hr class="hr-element" />

        <div>
          <h1 class="text-center mb-5">Explore public groups</h1>
          <v-row justify="space-around">
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
            <GroupCard />
          </v-row>
        </div>
      </div>
    </div>

    <!-- signed in -->
    <div v-else>
      <div class="mt-10">
        <h1 class="text-center mb-5">Public groups</h1>
        <v-row justify="space-around">
          <GroupCard />
          <GroupCard />
          <GroupCard />
          <GroupCard />
        </v-row>
      </div>

      <hr class="hr-element" />

      <div class="mt-10">
        <h1 class="text-center mb-5">Your groups</h1>
        <v-row justify="space-around">
          <GroupCard />
          <GroupCard />
          <GroupCard />
          <GroupCard />
          <GroupCard />
        </v-row>
      </div>
    </div>

    <v-dialog v-model="showSearchedResultsDialog" width="550" persistent>
      <v-card width="550" class="px-4 py-4 white--text" dark>
        <v-list v-if="users.length > 0">
          <v-list-item
            v-for="(user, index) in users"
            :key="index"
            class="listItem"
          >
            <v-list-item-title>
              <v-avatar size="28" color="white">
                <v-img
                  v-if="user.profile_url == ''"
                  :src="require(`../../public/userimg.png`)"
                ></v-img>
                <v-img v-else :src="user.profile_url"></v-img>
              </v-avatar>
              <span class="ml-2">
                {{ user.username }}
              </span>
            </v-list-item-title>
          </v-list-item>
        </v-list>
        <v-list v-else class="text-center">
          <v-list-item class="text-center">Not Found</v-list-item>
        </v-list>
      </v-card>

      <v-card-actions>
        <v-btn
          small
          class="white--text text-capitalize"
          dark
          @click="closeDialog()"
          >Close</v-btn
        >

        <span class="ml-auto">
          <v-btn
            v-if="currentPage > 1 && currentPage <= totalPages"
            small
            class="white--text text-capitalize mr-2"
            dark
            @click="previousPageButtonOnClick()"
          >
            Previous
          </v-btn>
          <v-btn
            v-if="currentPage >= 1 && currentPage < totalPages"
            small
            class="white--text text-capitalize"
            dark
            @click="nextPageButtonOnClick()"
          >
            Next
          </v-btn>
        </span>
      </v-card-actions>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";
import GroupCard from "../components/GroupCard.vue";

export default {
  name: "Home",

  components: {
    GroupCard,
  },

  data: () => ({
    users: [],
    searchText: "",
    totalPages: 0,
    currentPage: 1,

    showMenu: false,
    menuWidth: null,
    menuPositionX: null,
    menuPositionY: null,

    showSearchedResultsDialog: false,
  }),

  created() {
    // document.addEventListener("keyup", (event) => {
    //   if (event.key === "Enter") {
    //     this.searchUsersAcceptAnonymousMessage();
    //   }
    // });

    if (this.$store.state.user.accessToken == null) this.$router.push({ name: "SignIn" });
    else this.$router.push({ name: "Messages" })
  },

  methods: {
    findSearchElementPosition: function () {
      let element = document.getElementById("search-element");
      let rect = element.getBoundingClientRect();

      return {
        width: element.offsetWidth + 20,
        height: element.offsetHeight + 10,
        positionX: rect.left,
        positionY: rect.top,
      };
    },

    // search when typing
    searchUsersAcceptAnonymousMessageOnTyping: function () {
      if (this.searchText.trim() != "") {
        let position = this.findSearchElementPosition();

        this.menuWidth = position["width"];
        this.menuPositionX = position["positionX"];
        this.menuPositionY = position["positionY"] + position["height"];
        this.showMenu = true;

        axios
          .get("api-users/search-users-accept-anonymous-message-on-typing/", {
            params: {
              search_text: this.searchText,
            },
          })
          .then((res) => {
            if (res.data["results"]) {
              this.users = res.data["results"];
            }
          });
      } else {
        this.showMenu = false;
        this.menuWidth = null;
        this.menuPositionX = null;
        this.menuPositionY = null;
      }
    },

    // search when enter key press
    searchUsersAcceptAnonymousMessage: function () {
      if (this.searchText.trim() != "") {
        axios
          .get("api-users/search-users-accept-anonymous-message/", {
            params: {
              search_text: this.searchText,
              page: this.currentPage,
            },
          })
          .then((res) => {
            if (res.data["results"]) {
              this.users = res.data["results"];
              this.totalPages = res.data["total_pages"];
              this.showSearchedResultsDialog = true;
              this.showMenu = false;
            }
          });
      }
    },

    nextPageButtonOnClick: function () {
      this.currentPage = this.currentPage + 1;
      this.searchUsersAcceptAnonymousMessage();
    },

    previousPageButtonOnClick: function () {
      this.currentPage = this.currentPage - 1;
      this.searchUsersAcceptAnonymousMessage();
    },

    closeDialog: function () {
      this.currentPage = 1;
      this.showSearchedResultsDialog = false;
      this.totalPages = 0;
    },
  },
};
</script>

<style scoped>
.hr-element {
  background-color: grey;
  height: 1px;
  border: none;
  margin-top: 50px;
  margin-bottom: 50px;
}

.listItem {
  cursor: pointer;
}
.listItem:hover {
  background-color: rgb(63, 63, 63);
}
</style>
