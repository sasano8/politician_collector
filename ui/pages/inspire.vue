<template>
  <div>
    {{ notify }}
    <v-snackbar v-model="lastMessage" top>
      {{ lastMessage }}
      <template v-slot:action="{ attrs }">
        <v-btn v-bind="attrs"> Close </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { mapState, mapGetters } from "vuex";
export default Vue.extend({
  computed: {
    ...mapState(["notify"]),
    ...mapGetters("notify", ["lastMessage"]),
  },
});
</script>
