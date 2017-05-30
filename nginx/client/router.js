import Vue from "vue";
import VueRouter from "vue-router";
import * as AppView from "./components/appView/appView.vue";
import * as LoginView from "./components/loginView/loginView.vue";

Vue.use(VueRouter);

export default new VueRouter({
    mode: "history",
    routes: [{
        path: "/channel/:channelId",
        component: AppView,
        name: "channel",
        props: function (route) {
            return {
                channelName: "#general",
                channelDesc: "Discuss anything here :)",
                channelId: route.params.channelId
            }
        }
    }, {
        path: "/login",
        component: LoginView,
        name: "login",
        // TODO: maybe a better way to pass this props?
        props: {
            serverName: "Arc Community",
            serverDesc: "The official server for developement of arc"
        }
    },{
        // TODO: catch all should redirect to @me
        path: "*",
        component: {template: "<em>Sorry this url does not exist :(</em>"}
    }]
});
