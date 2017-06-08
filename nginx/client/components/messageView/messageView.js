import * as Message from "../message/message.vue";

export default {
    components: {
        message: Message
    },
    computed: {
        messages: function () {
            // use this to make a function in store which
            // returns messages for this channel only.
            // console.log(this.$props);
            return this.$store.getters.getMessagesFromChannel(this.$props.channelId);
        }
        // TODO: grouping needs to break after every hour
        // isGrouped: function () {
        //     return this.$store.getters.isSameAuthor;
        // }
    },
    props: ["channelName", "channelId"]
}
