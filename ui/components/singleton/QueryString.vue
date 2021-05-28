<!-- 指定したクエリパラメータを同期する -->
<template></template>
<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  props: {
    key: {
      type: String,
      default: "q",
    },
    value: undefined,
    empty: undefined,
  },
  components: {},
  watch: {
    $route: {
      immediate: true,
      handler(newValue, oldValue) {
        this.updateQuery(newValue.query[this.key], this.empty);
      },
    },
    value: {
      immediate: false,
      handler(newValue, oldValue) {
        this.updateQuery(newValue, oldValue);
      },
    },
  },
  methods: {
    updateQuery: function (newValue, oldValue) {
      let newValue2 = newValue;
      if (!newValue) {
        newValue2 = this.empty;
      }

      let query = Object.assign({}, this.$route.query);
      query[this.key] = newValue2;
      this.computedValue = newValue2;

      // 同じパスに移動した時、NavigationDuplicatedが発生する
      // 例外を無視させるため、空のコールバックを設定する
      this.$router.replace({ query }, () => {});
    },
  },
  computed: {
    computedValue: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      },
    },
  },
});
</script>
