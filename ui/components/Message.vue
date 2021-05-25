<template>
  <div>
    <v-snackbar v-bind:value="lastMessage" top timeout="3000">
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

/*
TODO: 複数のメッセージに対応させたい。現在は１つしか表示できず、複数のメッセージのコントロールができない。
*/