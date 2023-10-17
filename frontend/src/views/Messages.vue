<template>
  <v-container fill-height>
    <v-row align="center" justify-content="center">
      <v-col cols="12" class="mr-auto ml-auto">
        <div>
          <v-card class="px-0 py-0 white--text message-card">
            <v-layout>
              <v-navigation-drawer
                permanent
                style="background-color: rgb(95, 95, 95); height: 800px"
                id="navigation-drawer"
              >
                <v-list density="compact" nav>
                  <v-list-item
                    v-for="(i, index) in 20"
                    :key="index"
                    class="user-list pb-1"
                  >
                    <v-avatar size="36" color="white"></v-avatar>
                    <span class="white--text ml-2">Richard </span>
                  </v-list-item>
                  <v-list-item class="user-list pb-1">
                    <v-avatar size="36" color="white"></v-avatar>
                    <span class="white--text ml-2">Richard</span>
                  </v-list-item>
                  <v-list-item class="user-list pb-1">
                    <v-avatar size="36" color="white"></v-avatar>
                    <span class="white--text ml-2">Richard </span>
                  </v-list-item>
                </v-list>
              </v-navigation-drawer>
              <v-main style="height: 250px"></v-main>
            </v-layout>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Messages",
};
</script>

<style scoped>
.message-card {
  background-color: rgb(95, 95, 95);
  border-radius: 5px;
  height: 800px;
}
.user-list {
  border-bottom: solid;
  border-bottom-width: 1px;
  border-bottom-color: grey;
  cursor: pointer;
  font-size: 14px;
}
.user-list:hover {
  background-color: rgb(100, 100, 100);
}

#navigation-drawer::-webkit-scrollbar {
  width: 20px;
}
#navigation-drawer::-webkit-scrollbar-track {
  background-color: transparent;
}
#navigation-drawer::-webkit-scrollbar-thumb {
  background-color: #d6dee1;
  border-radius: 20px;
  border: 6px solid transparent;
  background-clip: content-box;
}
</style>