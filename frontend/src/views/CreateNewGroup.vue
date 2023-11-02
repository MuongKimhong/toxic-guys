<template>
  <v-container>
    <v-row align="center" justify-content="center">
      <v-col cols="8" class="mr-auto ml-auto">
        <div class="mt-10">
          <div class="text-center">
            <v-avatar size="120" color="white" class="ml-auto mr-auto">
              <v-img
                v-if="groupImage === null"
                :src="require(`../../public/groupimg.png`)"
              ></v-img>
              <v-img v-else :src="groupImageURL"></v-img>
            </v-avatar>

            <div class="text-center mt-5">
              <v-btn
                v-if="groupImage === null"
                small
                class="text-capitalize white--text"
                style="background-color: rgb(95, 95, 95)"
                @click="uploadImageBtnOnClick()"
              >
                Upload Image
              </v-btn>
              <v-btn
                v-else
                small
                class="text-capitalize white--text"
                style="background-color: rgb(95, 95, 95)"
                @click="uploadImageBtnOnClick()"
              >
                Change Image
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
            ></v-select>

            <v-textarea
              rounded
              outlined
              dark
              label="Description"
              v-model="groupDescription"
              counter="100"
              :error-messages="err.description"
            ></v-textarea>
          </div>

          <div class="text-center mt-6">
            <v-btn
              class="text-capitalize white--text"
              dark
              small
              @click="createGroup()"
            >
              Create Group
            </v-btn>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "CreateNewGroup",

  data: () => ({
    groupImage: null,
    groupImageURL: null,
    groupName: "",
    groupType: "",
    groupDescription: "",

    err: {
      name: "",
      type: "",
      description: "",
    },
  }),

  methods: {
    uploadImageBtnOnClick: function () {
      let self = this;
      let input = document.createElement("input");
      input.type = "file";
      input.accept = ".jpg,.JPEG,.png";
      input.onchange = () => {
        let files = Array.from(input.files);
        self.groupImage = files[0];
        self.groupImageURL = URL.createObjectURL(files[0]);
        input.remove();
      };
      input.click();
    },

    createGroup: function () {
      this.err = { name: "", type: "", description: "" };

      if (this.groupName.trim() === "") {
        this.err.name = "Please enter group name";
        return;
      } else if (this.groupName.length > 20) {
        this.err.name = "Name exceeds word limit";
        return;
      } else if (this.groupType.trim() === "") {
        this.err.type = "Please choose group type";
        return;
      } else if (this.groupDescription.length > 100) {
        this.err.type = "Description exceeds word limit";
        return;
      }

      var formData = new FormData();
      formData.append("group_name", this.groupName);
      formData.append("group_type", this.groupType);
      formData.append("group_description", this.groupDescription);
      formData.append("group_profile", this.groupImage);

      axios
        .post("api-groups/create-group/", formData, {
          headers: {
            "content-type": "multipart/form-data",
            Authorization: `Bearer ${this.$store.state.user.accessToken}`,
          },
        })
        .then((res) => {
          if (res.data["group_created"]) {
            this.$router.push({ name: "Messages" }).catch(() => {});
          }
        });
    },
  },
};
</script>