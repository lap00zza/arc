<template>
    <div class="message">
        <div class="message__author-avatar">
            <img v-bind:src="avatar" draggable="false">
        </div>
        <div class="message__body">
            <div class="message__meta">
                <span class="message__author">{{ author.username }}</span>
                <span class="message__local-time">{{ localTime }}</span>
            </div>
            <div class="message__content">{{ content }}</div>
        </div>
    </div>
</template>
<script>
    export default {
        props: ["author", "content", "timestamp"],
        computed: {
            avatar: function () {
                return "https://www.gravatar.com/avatar/" + this.$props.author.avatar;
            },
            localTime: function () {
                return new Date(this.$props.timestamp).toLocaleTimeString();
            }
        }
    }
</script>
