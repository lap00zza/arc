<template>
    <div class="message-view" v-auto-scroll>
        <message v-for="message in messages"
                 v-bind:message="message.data"
                 v-bind:key="message.id">
        </message>
    </div>
</template>
<script src="./messageView.js"></script>