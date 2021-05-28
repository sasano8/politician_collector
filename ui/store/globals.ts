import { getterTree, mutationTree, actionTree } from "typed-vuex";

export const state = () => ({
  clipped: false,
  drawer: false,
  fixed: false,
});

export type RootState = ReturnType<typeof state>;

export const getters = getterTree(state, {
  clipped: (state) => state.clipped,
  drawer: (state) => state.drawer,
  fixed: (state) => state.fixed,
});

export const mutations = mutationTree(state, {
  setClipped(state, val: boolean): void {
    state.clipped = val;
  },
  setDrawer(state, val: boolean): void {
    state.drawer = val;
  },
  setFixed(state, val: boolean): void {
    state.fixed = val;
  },
});

export const actions = actionTree(
  { state, getters, mutations },
  {
    setClipped(context, val: boolean) {
      context.commit("setClipped", val);
    },
    setDrawer(context, val: boolean) {
      context.commit("setDrawer", val);
    },
    setFixed(context, val: boolean) {
      context.commit("setFixed", val);
    },
  }
);
