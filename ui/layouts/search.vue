<template>
  <v-app dark>
    <v-navigation-drawer v-model="drawer" :clipped="clipped" fixed app>
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar :clipped-left="clipped" fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <!-- <v-btn icon @click.stop="miniVariant = !miniVariant">
        <v-icon>mdi-{{ `chevron-${miniVariant ? "right" : "left"}` }}</v-icon>
      </v-btn> -->
      <!-- <v-btn icon @click.stop="clipped = !clipped">
        <v-icon>mdi-application</v-icon>
      </v-btn> -->
      <!-- <v-btn icon @click.stop="fixed = !fixed">
        <v-icon>mdi-minus</v-icon>
      </v-btn> -->

      <v-toolbar-title v-text="title"> </v-toolbar-title>
      <v-spacer />
      <query-string v-model="query_string"></query-string>
      <v-text-field
        v-model="query_string"
        width="100%"
        flat
        solo-inverted
        hide-details
        label="検索キーワード"
      ></v-text-field>

      <v-spacer />

      <!-- <v-btn icon @click.stop="rightDrawer = !rightDrawer">
        <v-icon>mdi-menu</v-icon>
      </v-btn> -->
    </v-app-bar>
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
    <!-- <v-navigation-drawer v-model="rightDrawer" :right="right" temporary fixed>
      <v-list>
        <v-list-item @click.native="right = !right">
          <v-list-item-action>
            <v-icon light> mdi-repeat </v-icon>
          </v-list-item-action>
          <v-list-item-title>Switch drawer (click me)</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer> -->
    <v-footer :absolute="!fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
    <message></message>
  </v-app>
</template>

<script>
import Message from "../components/Message.vue";
import QueryString from "../components/singleton/QueryString.vue";

export default {
  components: { Message, QueryString },
  data() {
    return {
      query_string: null,
      items: [
        {
          icon: "mdi-apps",
          title: "Welcome",
          to: "/",
        },
        {
          icon: "mdi-chart-bubble",
          title: "Inspire",
          to: "/inspire",
        },
        {
          icon: "mdi-apps",
          title: "全文検索",
          to: "/search",
        },
      ],
      // miniVariant: false,
      // right: true,
      // rightDrawer: false,
      title: "政治家検索",
    };
  },
  computed: {
    clipped: {
      get() {
        return this.$accessor.globals.clipped;
      },
      set(val) {
        this.$accessor.globals.setClipped(val);
      },
    },
    drawer: {
      get() {
        return this.$accessor.globals.drawer;
      },
      set(val) {
        this.$accessor.globals.setDrawer(val);
      },
    },
    fixed: {
      get() {
        return this.$accessor.globals.fixed;
      },
      set(val) {
        this.$accessor.globals.setFixed(val);
      },
    },
  },
};
</script>
