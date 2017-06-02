export default {
    data: function () {
        return {
            status: "",
            in_progress: false,
            email: "",
            password: ""
        }
    },
    methods: {
        onSubmit: function (e) {
            e.preventDefault();
            var instance = this;
            instance.in_progress = true;
            
            // NOTE TO SELF: vue resource automatically sets the content-type
            // header to application/json. So we don't have to set it manually.
            this.$http
                .post("/api/v1/auth/login", {
                    email: instance.email,
                    password: instance.password
                })
                .then(function (resp) {
                    console.log(resp);
                    window.localStorage.setItem("token", resp.body["token"]);
                    this.$router.push({
                        name: "channel",
                        params: {
                            channelId: "general"
                        }
                    });
                })
                .catch(function (e) {
                    instance.in_progress = false;
                    instance.status = e.data["error"];
                    console.debug(e)
                })
        }
    }
}
