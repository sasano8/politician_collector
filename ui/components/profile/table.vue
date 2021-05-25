<template>
  <div>
    <v-data-table
      :headers="filterdHeaders"
      :items="extendRows"
      item-key="_id"
      class="elevation-1"
      :loading="loading"
    >
      <template v-slot:[`item.profile.議員氏名`]="{ item }">
        <NuxtLink
          :to="{ name: 'profile-id', params: { id: item['profile.id'][0] } }"
          >{{ item["profile.議員氏名"].toString() }}</NuxtLink
        >
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  props: {
    queryString: { type: String, default: null },
    loading: { type: Boolean, default: false },
  },
  data() {
    return {
      rows: [],
      headers: [
        {
          value: "_id",
          text: "_id",
          align: "start",
          sortable: false,
          hide: true,
        },
        {
          value: "profile.id",
          text: "id",
          align: "start",
          sortable: false,
          hide: true,
        },
        {
          value: "profile.議員氏名",
          text: "議員氏名",
          align: "start",
          sortable: false,
          hide: false,
        },
        {
          value: "profile.会派",
          text: "会派",
          align: "start",
          sortable: false,
          hide: false,
        },
      ],
    };
  },
  computed: {
    filterdHeaders() {
      return this.headers.filter((s) => !s.hide);
    },
    extendRows() {
      return this.rows;
    },
  },
  watch: {
    queryString: {
      immediate: true,
      async handler(queryString) {
        let q = queryString;
        let rows = null;
        if (q === undefined || q === null || q === "") {
          q = "";
        }

        if (q === "") {
          this.rows = [];
        } else {
          const url = "http://localhost:8080/person/search_profile";
          const tmp = await this.$axios.$get(url, {
            params: { 議員氏名: q, size: 5 },
          });
          this.rows = tmp.hits.hits;
        }
      },
    },
  },
};
</script>
