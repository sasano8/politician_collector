<template>
  <v-container>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <searchbox v-model="query_string"></searchbox>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <div class="text-center"></div>
        <v-card> </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <div class="text-center"></div>
        <v-card>
          <profile-table :queryString="query_string"></profile-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import ProfileTalbe from "../../components/profile/table.vue";
import Searchbox from "../../components/searchbox.vue";

export default Vue.extend({
  layout(context) {
    return "default";
  },
  data() {
    return {
      query_string: "",
      rows: [],
    };
  },
  components: {
    Searchbox,
    ProfileTalbe,
  },
  created() {
    // const age = this.$accessor.age.age;
    // const res = this.$accessor.age.hoge();
    this.query_string = this.$route.query["q"];
  },
  watch: {
    query_string(query_string) {
      let query = {};
      if (query_string === undefined || query_string === "") {
        query["q"] = undefined;
      } else {
        query["q"] = query_string;
      }
      this.$router.push({ path: this.$route.path, query });
    },
  },
});
</script>
