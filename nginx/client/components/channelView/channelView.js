import * as MessageView from "../messageView/messageView.vue";
import * as MessageSend from "../messageSend/messageSend.vue";

export default {
    data: function() {
        return {
            channel_loaded: true
        }
    },
    components: {
        messageView: MessageView,
        messageSend: MessageSend
    },
    // created: function () {
    //     console.log("created");
    //     var ctx = this;
    //     setTimeout(function () {
    //         ctx.channel_loaded = true;
    //     }, 2000)
    // },
    // beforeUpdate: function () {
    //     console.log("beforeUpdate");
    //     this.channel_loaded = false;
    // },
    // updated: function () {
    //     console.log("updated");
    //     this.channel_loaded = true;
    // },
    // TODO: I can probably make it work by using Vuex and storing a onLoad state
    // TODO: work on the loader which will be used while fetching is in progress
    computed: {
        channel: function () {
            var channel_details = this.$store.getters.getChannel(this.$props.channelId);
            if (channel_details) {
                // this.channel_loaded = true;
                return channel_details;
            }
          
        }
    },
    props: ["channelName", "channelDesc", "channelId"]
}