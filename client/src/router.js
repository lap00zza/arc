import Vue from "vue";
import VueRouter from "vue-router";
import * as ChannelView from "./components/channelView/channelView.vue";

Vue.use(VueRouter);

export default new VueRouter({
    routes: [{
        path: "/channel/:channelId",
        component: ChannelView,
        name: "channel",
        props: function (route) {
            return {
                channelName: "#general",
                channelDesc: "Discuss anything here :)",
                channelId: route.params.channelId
            }
        }
    }]
});
