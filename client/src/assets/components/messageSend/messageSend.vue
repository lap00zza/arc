<template>
    <div class="container">
        <input type="text" v-model="sendMessageInput" v-on:keydown="sendMessage" placeholder="Send a message!">
    </div>
</template>
<script src="./messageSend.js"></script>
