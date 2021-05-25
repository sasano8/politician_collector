import { getterTree, mutationTree, actionTree } from "typed-vuex";

export const state = () => ({
  messages: [] as string[]
});

export type RootState = ReturnType<typeof state>;

export const getters = getterTree(state, {
  exists: (state) => state.messages.length !== 0,
  firstMessage: (state) => state.messages[0],
  lastMessage: (state) => state.messages[state.messages.length - 1]
});

export const mutations = mutationTree(state, {
  setMessages(state, messages: string[]): void {
    state.messages = messages
  },
  pushMessage(state, message: string): void {
    state.messages.push(message)
  },

});

export const actions = actionTree(
  { state, getters, mutations },
  {
    pushMessage(context, message: string) {
      context.commit("pushMessage", message)
    },
    shiftMessage(context) {
      if (context.state.messages.length === 0) {
        return null
      } else {
        const msg = context.state.messages.shift();
        context.commit("setMessages", context.state.messages)
        return msg
      }
    }
  }
);


