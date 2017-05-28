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
        onInput: function () {
            var textArea = this.$el.getElementsByTagName("textarea")[0];
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
                var textArea = this.$el.getElementsByTagName("textarea")[0];
                
                // The following regex removes any whitespace character at 
                // the start and at the end of the message.
                var message = this.sendMessageInput.replace(/^\s+|\s+$/g, "");
                
                // We won't send blank messages.
                // TODO: need a server side validation for blank messages
                if (message.length === 0) {
                    return false;
                }
                var options = {
                    headers: {
                        "Content-type": "application/x-www-form-urlencoded"
                    }
                };
                // encodeURIComponent to fix the bug when sending the character & (ampersand).
                // TODO: maybe send the payload as json (like how discord does it)
                this
                    .$http.post("/api/messages", "author=anonymous&content=" + encodeURIComponent(message), options)
                    .then(function success() {
                        console.log("Message successfully sent!");
                        
                    }, function  error(e) {
                        console.debug(e);
                    });
                
                // empty the text area once we send 
                // the message, and then resize it.
                this.sendMessageInput = "";
                resetTextarea(textArea);
            }
        }
    }
}
