<template>
    <div class="message-view" v-auto-scroll>
        <div class="blank_channel_template">
            <h1 class="channel_name">#{{ channelName }}</h1>
            <p>Welcome to the beginning of #{{ channelName }}. Message away! Remember basic markdown is supported.</p>
        </div>

        <!-- TODO: redo this grouping in discord's style -->
        <message v-for="message in messages"
                 v-bind:key="message.id"
                 v-bind:author="message.author"
                 v-bind:content="message.content"
                 v-bind:timestamp="message.timestamp">
        </message>

    </div>
</template>
<script src="./messageView.js"></script>
