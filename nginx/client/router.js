import Vue from "vue";
import VueRouter from "vue-router";
import * as AppView from "./components/appView/appView.vue";
import * as LoginView from "./components/loginView/loginView.vue";
import * as RegisterView from "./components/registerView/registerView.vue";

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
        name: "login"
    },{
        path: "/register",
        component: RegisterView,
        name: "register"
    },{
        // TODO: catch all should redirect to @me
        path: "*",
        component: {template: "<em>Sorry this url does not exist :(</em>"}
    }]
});
