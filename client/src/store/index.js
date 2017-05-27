import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const state = {
    messages: []
};

const mutations = {
    addMessage: function (state, message) {
        state.messages.push(message)
    }
};


export default new Vuex.Store({
    state: state,
    mutations: mutations
})
