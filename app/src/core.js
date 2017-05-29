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
import VueResource from "vue-resource";
import store from "./store";
import router from "./router";

Vue.use(VueResource);

// A custom directive that auto scrolls 
// the message view when new message is
// added to it.
Vue.directive("auto-scroll", {
    componentUpdated: function (el) {
        // console.log(el, el.scrollHeight);
        el.scrollTop = el.scrollHeight;
    }
});

var app = new Vue({
    data: {
        messages: []
    },
    router: router,
    store: store
}).$mount("#app-mount");
