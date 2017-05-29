<template>
    <div class="app_container">
        <div class="channel_container flex-column">
            <div class="flex-column flex-spacer">
                <ul>
                    <li><router-link to="/channel/develop">#develop</router-link></li>
                    <li><router-link to="/channel/github_updates">#github_updates</router-link></li>
                    <li><router-link to="/channel/fun">#fun</router-link></li>
                </ul>
            </div>
            <!-- Some good ol' credits -->
            <div class="credits flex-column">
                <span class="title">arc!</span>
                <span class="meta">
                    made with <3 by <a href="https://github.com/lap00zza" target="_blank">@lap00zza</a>
                </span>
            </div>
        </div>
        <!---->
        <channel-view :channelName="channelName" :channelDesc="channelDesc" :channelId="channelId"></channel-view>
    </div>
</template>
<script>
    import * as ChannelView from "../channelView/channelView.vue";
    export default {
        components: {
            channelView: ChannelView
        },
        props: ["channelName", "channelDesc", "channelId"]
    }
</script>