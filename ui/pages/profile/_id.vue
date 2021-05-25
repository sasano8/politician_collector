<template>
  <profile-detail :id="$route.params.id"></profile-detail>
</template>

<script lang="ts">
import Vue from "vue";
import ProfileDetail from "../../components/profile/detail.vue";

export default Vue.extend({
  layout(context) {
    return "default";
  },
  data() {
    return {
      id: null,
    };
  },
});
</script>
