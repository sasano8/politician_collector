<template>
  <div>
    <v-data-table
      :headers="filterdHeaders"
      :items="extendRows"
      item-key="_id"
      class="elevation-1"
      :loading="loading"
      loading-text="検索中"
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
  },
  data() {
    return {
      loading: true,
      queue: [],
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
          q = null;
        }
        this.updateTable(q);
      },
    },
  },
  mounted() {
    window.setInterval(this.updateQueue, 500);
  },
  methods: {
    async updateTable(queryString) {
      let p = null;
      if (queryString === null) {
        p = new Promise(function (resolve, reject) {
          resolve([]);
        });
      } else {
        const url = "http://localhost:8080/person/search_profile";
        p = this.$axios
          .$get(url, {
            params: { 議員氏名: queryString, size: 5 },
          })
          .then((res) => res.hits.hits);
      }
      this.queue.push(p);
    },
    updateQueue() {
      // 非同期に実行すると、応答結果が前後することがあるので、最終入力のみ処理する

      // キューが処理済みの場合は何もしない
      if (this.queue.length === 0) {
        this.loading = false;
        return;
      }

      // 実行するタスクは１つのみ
      if (this.queue.length !== 1) {
        this.loading = true;
        const p = this.queue[this.queue.length - 1];
        this.rows = [];
        this.queue = [p];
        return;
      }

      if (this.queue.length === 1) {
        this.loading = true;
        const p = this.queue[this.queue.length - 1];
        this.queue = [];
        p.then((value) => {
          this.rows = value;
          this.loading = false;
        });
      }
    },
  },
};
</script>
