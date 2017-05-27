<template>
    <div class="message-send">
        <div class="widget">
            <textarea rows="1" v-model="sendMessageInput"
                      v-on:input="onInput" v-on:keydown="onKeyDown"
                      placeholder="Message #general"></textarea>
            <div class="emojis"></div>
        </div>
        <div class="meta">press <code>enter</code> to send message</div>
    </div>
</template>
<script src="./messageSend.js"></script>
