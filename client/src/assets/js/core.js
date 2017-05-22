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

var ws_url = "ws://" + window.location.hostname + "/ws";
var ws = new WebSocket(ws_url);
var vm = document.getElementById("viewMessage");
var sm = document.getElementById("sendMessage");

function send(data, event="message") {
    ws.send(JSON.stringify({
        event: event,
        data: data
    }))
}
function parse(data) {
    return JSON.parse(data)
}

ws.onmessage = function (event) {
    console.log(event);

    var parsed = parse(event.data);
    var messageObj = document.createElement("div");

    messageObj.classList.add("message");
    messageObj.innerHTML =
        `<div>${parsed.data}</div>`;

    vm.appendChild(messageObj);

    // once we append the message, we scroll
    // to the bottom
    vm.scrollTop = vm.scrollHeight;
};

sm.addEventListener("keydown", function (e) {

    // if the user presses the enter key, we send the
    // message back to the WebSocket server

    if (e.keyCode === 13) {
        send(this.value);
        this.value = "";
    }
});