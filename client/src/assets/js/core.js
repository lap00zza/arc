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