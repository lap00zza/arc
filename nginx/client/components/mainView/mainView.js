import * as ChannelView from "../channelView/channelView.vue";
import * as Channel from "../channel/channel.vue";
import { startWSConnection } from "../../connection";
import store from "../../store";

export default {
    components: {
        channelView: ChannelView,
        channel: Channel
    },
    computed: {
        channels: function () {
            return this.$store.state.channels;
        },
        myAvatar: function () {
            return this.$store.state.myInfo.avatar;
        },
        myName: function () {
            return this.$store.state.myInfo.username;
        }
    },
    created: function () {
        // TODO: Websocket should only receive data after verifying token
        // TODO: api calls should probably be made using vuex actions
        var token = window.localStorage.getItem("token");
        console.log("token: ", token);
        if (token) {
            this.$http
                .get("/api/v1/myInfo", {
                    headers: {
                        Authorization: "Bearer " + token
                    }
                })
                .then(function (resp) {
                    console.log(resp);
                    store.commit("updateMyInfo", {
                        id: resp.data.id,
                        username: resp.data.username,
                        avatar: "https://www.gravatar.com/avatar/" + resp.data.avatar
                    });
                    store.commit("addChannel", resp.data.channels);
                })
                .catch(function (e) {
                    console.debug(e)
                });

            // Start the websocket connection.
            // TODO: need to add reconnecting websocket
            startWSConnection();
        } else {
            this.$router.push({
                name: "login"
            })
        }
    },
    props: ["channelName", "channelDesc", "channelId"]
} 