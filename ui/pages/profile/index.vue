<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  layout(context) {
    return "default";
  },
  asyncData({ error, params }) {
    error({ statusCode: 404 });
  },
});
</script>
