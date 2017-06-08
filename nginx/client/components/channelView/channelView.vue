<template>
    <div v-if="!channel_loaded" class="flex-row flex-spacer main__channel__loader">
        <img src="/assets/images/three-dots.svg">
    </div>
    <div v-else class="main_container flex-spacer flex-column">
        <div class="info flex-row">
            <div class="info-item toggle-channel-list" style="display: none;">
                <img src="/assets/images/menu_toggle.png">
            </div>
            <div class="info-item">
                <div class="name">#{{ channel.name }}</div>
                <div class="description">{{ channel.description }}</div>
            </div>
        </div>
        <div class="flex-spacer flex-row">
            <!-- messages needs to be bound as they will change over time. -->
            <div class="flex-spacer flex-column">
                <div class="view flex-column flex-spacer">
                    <message-view v-bind:channelName="channel.name" v-bind:channelId="channel.id"></message-view>
                </div>
                <div class="message-send-wrapper">
                    <message-send v-bind:channelId="channel.id"></message-send>
                </div>
            </div>
            <div class="users flex-column">

            </div>
        </div>
    </div>
</template>
<script src="./channelView.js"></script>
