<template>
    <div class="message" v-once>
        <div class="profile_image">
            <img src="/src/assets/images/user_place_holder.png">
        </div>
        <div class="message_body">
            <div class="author">Anonymous</div>
            <div class="content">{{ message.content }}</div>
        </div>
    </div>
</template>
<script>
    export default {
        props: ["message"]
    }
</script>
