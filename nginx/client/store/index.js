import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const state = {
    messages: [],
    myInfo: {
        id: "",
        username: "",
        avatar: ""
    }
};

const mutations = {
    addMessage: function (state, message) {
        state.messages.push(message)
    },
    /**
     * This method can be used to independently update myInfo or 
     * update them all at once.
     * 
     * For updating independently, make sure to pass Null to the 
     * other params.
     * 
     * @param state {Object}
     * @param info {Object}
     */
    updateMyInfo: function (state, info) {
        if (info.id) {
            state.myInfo.id = info.id;
        }
        if (info.username) {
            state.myInfo.username = info.username;
        }
        if (info.avatar) {
            state.myInfo.avatar = info.avatar;
        }
        
    }
};


export default new Vuex.Store({
    state: state,
    mutations: mutations
})
