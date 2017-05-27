<template>
    <div class="main_container flex-spacer flex-column">
        <div class="info flex-row">
            <div class="info-item toggle-channel-list" style="display: none;">
                <img src="/src/assets/images/menu_toggle.png">
            </div>
            <div class="info-item">
                <div class="name">{{ channelName }}</div>
                <div class="description">{{ channelId }} | <em>{{ channelDesc }}</em></div>
            </div>
        </div>
        <div class="flex-spacer flex-row">
            <!-- messages needs to be bound as they will change over time. -->
            <div class="flex-spacer flex-column">
                <div class="view flex-column flex-spacer">
                    <message-view v-bind:messages="message_stack"></message-view>
                </div>
                <div class="message-send-wrapper">
                    <message-send></message-send>
                </div>
            </div>
            <div class="users flex-column">

            </div>
        </div>
    </div>
</template>
<script>
    import * as MessageView from "../messageView/messageView.vue";
    import * as MessageSend from "../messageSend/messageSend.vue";
    export default {
        components: {
            messageView: MessageView,
            messageSend: MessageSend
        },
        computed: {
            message_stack: function () {
                // use this to make a function is store which
                // returns messages for this channel only.
                console.log(this.$props);
                return this.$store.state.messages;
            }
        },
        props: ["channelName", "channelDesc", "channelId"]
    }
</script>