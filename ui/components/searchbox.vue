<template>
  <v-form :value="valid">
    <v-container>
      <v-row>
        <v-col cols="12" md="12">
          <v-text-field
            label="検索キーワード"
            v-model="computedValue"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
export default {
  props: {
    valid: false,
    value: "",
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
};
</script>