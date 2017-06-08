import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const state = {
    channels: [],
    messages: [],
    myInfo: {
        id: "",
        username: "",
        avatar: ""
    }
};

const mutations = {
    addChannel: function (state, channel) {
        // If its an array, like in the case of the initial setup, 
        // then we iterate and push. Else we just push it normally.
        if (channel instanceof Array) {
            channel.forEach(function (item) {
                state.channels.push(item)
            })
        } else {
            state.channels.push(channel)
        }
    },
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

const getters = {
    /***
     * A simple getter function that checks whether the last message and the
     * second last message are by the same author. This is used while grouping
     * the messages.
     *
     * @param state
     * @returns {boolean}
     */
    isSameAuthor: function (state) {
        var result = false;
        try {
            result = state.messages[state.messages.length - 1].author.id === state.messages[state.messages.length - 2].author.id;
        } catch (e) {
            //
        }
        return result
    },
    getChannel: function (state) {
        // You can also pass arguments to getters by returning a function.
        // This is particularly useful when you want to query an array in
        // the store: https://vuex.vuejs.org/en/getters.html
        return function (channelId) {
            for (var i = 0; i < state.channels.length; i++) {
                if (state.channels[i].id == channelId) {
                    return state.channels[i];
                }
            }
            return null
        }
    },
    // TODO: grouping should be done from here and not from template
    getMessagesFromChannel: function (state) {
        return function (channelId) {
            var message_list= [];
            for (var i = 0; i < state.messages.length; i++) {
                if (state.messages[i].channel_id == channelId) {
                    // console.log(channelId, state.messages[i]);
                    message_list.push(state.messages[i]);
                }
            }
            return message_list;
        }
    }
};

export default new Vuex.Store({
    state: state,
    mutations: mutations,
    getters: getters
})
