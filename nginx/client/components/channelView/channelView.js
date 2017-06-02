import * as MessageView from "../messageView/messageView.vue";
import * as MessageSend from "../messageSend/messageSend.vue";
import { startWSConnection } from "../../connection";
import store from "../../store";

export default {
    components: {
        messageView: MessageView,
        messageSend: MessageSend
    },
    computed: {
        message_stack: function () {
            // use this to make a function in store which
            // returns messages for this channel only.
            // console.log(this.$props);
            return this.$store.state.messages;
        }
    },
    created: function () {
        // TODO: Websocket should only receive data after verifying token
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
                        avatar: resp.data.avatar
                    })
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