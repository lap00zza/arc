/**
 *  arc - dead simple chat
 *  Copyright (C) 2017 Jewel Mahanta <jewelmahanta@gmail.com>
 *
 *  This file is part of arc.
 *
 *  arc is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  arc is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with arc.  If not, see <http://www.gnu.org/licenses/>.
 */
import Vue from "vue";
// import VueRouter from "vue-router";
import VueResource from "vue-resource";
import * as MessageView from "../components/messageView/messageView.vue";
import * as MessageSend from "../components/messageSend/messageSend.vue";

// Vue.use(VueRouter);
Vue.use(VueResource);

// const router = new VueRouter({
//     routes: [
//         {path: "/", component: Home},
//         {path: "/browse", component: Browse}
//     ]
// });

// A custom directive that auto scrolls 
// the message view when new message is
// added to it.
Vue.directive("auto-scroll", {
    componentUpdated: function (el) {
        // console.log(el, el.scrollHeight);
        el.scrollTop = el.scrollHeight;
    }
});

var arc = new Vue({
    data: {
        messages: []
    },
    components: {
        messageView: MessageView,
        messageSend: MessageSend
    }
}).$mount("#app-mount");

var ws_url = "ws://" + window.location.hostname + "/ws";
var ws = new WebSocket(ws_url);

function parse(data) {
    return JSON.parse(data)
}

// We parse all the incoming events here and
// distribute it to the various event handlers.
ws.onmessage = function (event) {
    console.log(event);
    var parsed = parse(event.data);
    
    switch (parsed.type) {
        case "ready":
            arc.messages.push({
                id: parsed.s, 
                data: parsed.data
            });
            break;

        case "message":
            arc.messages.push({
                id: parsed.s, 
                data: parsed.data
            });
            break;
    }
};
