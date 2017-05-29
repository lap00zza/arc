export default {
    methods: {
        onSubmit: function (e) {
            e.preventDefault();

            // TODO: remember form data might now work in all browsers
            var form = new FormData(e.target);
            this.$http.post("/api/v1/auth/login", form)
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
        }
    },
    props: ["serverName", "serverDesc"]
}
