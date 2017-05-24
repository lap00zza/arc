export default {
    data: function () {
        return {
            sendMessageInput: ""
        }
    },
    methods: {
        sendMessage: function (e) {
            // Capture the instance
            var instance = this;
            
            // When the user presses enter, 
            // we send the message
            if (e.keyCode === 13) {
                var options = {
                    headers: {
                        "Content-type": "application/x-www-form-urlencoded"
                    }
                };
                instance
                    .$http.post("/api/messages", "author=anonymous&content=" + instance.sendMessageInput, options)
                    .then(function success() {
                        instance.sendMessageInput = "";
                    }, function  error(e) {
                        console.debug(e);
                    });
            }
        }
    }
}
