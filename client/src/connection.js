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
import store from "./store";

var ws = null;

function parse(data) {
    return JSON.parse(data)
}

function initializeListeners() {
    // We parse all the incoming events here and
    // distribute it to the various event handlers.
    ws.onmessage = function (event) {
        console.log(event);
        var parsed = parse(event.data);

        switch (parsed.type) {
            case "ready":
                store.commit("addMessage", {
                    id: parsed.s,
                    data: parsed.data
                });
                break;

            case "message":
                store.commit("addMessage", {
                    id: parsed.s,
                    data: parsed.data
                });
                break;
        }
    };

}

export function startWSConnection() {
    var ws_url = "ws://" + window.location.hostname + "/ws";
    ws = new WebSocket(ws_url);
    initializeListeners();
}