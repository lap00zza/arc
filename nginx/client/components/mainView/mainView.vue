<template>
    <div class="app_container">
        <div class="sidebar flex-column">
            <div class="flex-row sidebar__myInfo">
                <div class="flex-column avatar">
                    <img v-bind:src="myAvatar" draggable="false">
                    <div class="status_icon status-online"></div>
                </div>
                <div class="flex-column flex-spacer name_and_status">
                    <div class="flex-row name">{{ myName }}</div>
                    <div class="flex-row status">Checking out arc!</div>
                </div>
                <!--<div class="flex-column quick_notify_opt">
                    [ X ]
                </div>-->
            </div>
            <div class="flex-column flex-spacer">
                <div class="sidebar__channels">
                    <div class="header">CHANNELS</div>
                    <div class="wrapper">
                        <channel v-for="channel in channels"
                                 v-bind:key="channel.id"
                                 v-bind:id="channel.id"
                                 v-bind:name="channel.name">
                        </channel>
                    </div>
                </div>
            </div>
            <!-- Some good ol' credits -->
            <div class="sidebar__credits flex-column">
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
<script src="./mainView.js"></script>
