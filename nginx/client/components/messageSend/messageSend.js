function autoSizeTextarea(el) {
    // console.log(el, el.scrollHeight);
    if (el.scrollHeight < 100) {
        el.style.overflowY = "hidden";
        el.style.height = "auto";
        el.style.height = el.scrollHeight + "px";
    } else {
        el.style.overflowY = "scroll"
    }
}

function resetTextarea(el) {
    el.style.overflowY = "hidden";
    el.style.height = "auto";
}

export default {
    data: function () {
        return {
            sendMessageInput: ""
        }
    },
    methods: {
        onInput: function (e) {
            var textArea = e.target;
            autoSizeTextarea(textArea);
        },
        onKeyDown: function (e) {
            // NOTE: 'this' refers to this entire component

            // When the user presses enter without holding the shift key, 
            // we send the message. Else, we do nothing which translates 
            // to new line being added.
            if (e.keyCode === 13 && !e.shiftKey) {
                // prevent the default newline that is added
                // to the textarea when enter key is pressed.
                e.preventDefault();
                var textArea = e.target;
                var ctx = this;

                var chan_id = this.$props.channelId;

                // The following regex removes any whitespace character at 
                // the start and at the end of the message.
                var message = this.sendMessageInput.replace(/^\s+|\s+$/g, "");

                // We won't send blank messages.
                // TODO: need a server side validation for blank messages
                if (message.length === 0) {
                    return false;
                }

                // TODO: maybe send the payload as json (like how discord does it)
                this.$http
                    .post(`/api/v1/channel/${chan_id}/messages`, {
                        content: message
                    }, {
                        headers: {
                            Authorization: "Bearer " + window.localStorage.getItem("token")
                        }
                    })
                    .then(function success() {
                        console.log("Message successfully sent!");

                    }, function error(e) {
                        console.debug(e);
                        if (e.status === 401) {
                            ctx.$router.push({
                                name: "login"
                            })
                        }
                    });

                // empty the text area once we send 
                // the message, and then resize it.
                this.sendMessageInput = "";
                resetTextarea(textArea);
            }
        }
    },
    props: ["channelId"]
}
