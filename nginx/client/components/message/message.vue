<template>
    <div class="message" v-once>
        <div class="profile_image">
            <img v-bind:src="avatar">
        </div>
        <div class="message_body">
            <div class="author">{{ message.author.username }}</div>
            <div class="content">{{ message.content }}</div>
        </div>
    </div>
</template>
<script>
    export default {
        props: ["message"],
        computed: {
            avatar: function () {
                return "https://www.gravatar.com/avatar/" + this.$props.message.author.avatar
            }
        }
    }
</script>
