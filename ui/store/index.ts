import { getAccessorType } from "typed-vuex";

// 例えば、store/age.ts のようなサブモジュールが存在する場合、
// ここで import しておきます。
import * as globals from "~/store/globals";
import * as notify from "~/store/notify";

// ここでは、state, getters, mutations, actions の記法は省略しています。
// 記法については、後ほど記述する store/age.ts を参照してください。
// これらは、たとえ必要なくても、以下のように空でいいので、必ず記述してください。
export const state = () => {
  return {};
};

export const getters = {
  //
};

export const mutations = {
  //
};

export const actions = {
  //
};

export const accessorType = getAccessorType({
  state,
  getters,
  mutations,
  actions,
  modules: {
    // import したサブモジュールはここに記述します。
    globals,
    notify,
  },
});
