<!-- TODO: implement auto-scroll -->
<template>
    <div id="viewMessage">
        <message v-for="message in messages"
                 v-bind:message="message.data"
                 v-bind:key="message.id">
        </message>
    </div>
</template>
<script src="./messageView.js"></script>