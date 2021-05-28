<template>
  <v-container>
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
          <profile-table :queryString="$route.query.q"></profile-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import ProfileTalbe from "../../components/profile/table.vue";

export default Vue.extend({
  layout(context) {
    return "search";
  },
  components: {
    ProfileTalbe,
  },
});
</script>
