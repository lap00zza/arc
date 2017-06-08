<template>
    <div class="flex-row channel" draggable="true">
        <router-link v-bind:to="channel_url">
            <span class="flex-column flex-spacer channel__name">#{{ name }}</span>
        </router-link>
    </div>
</template>
<script>
    export default {
        computed: {
            channel_url: function () {
                return "/channel/" + this.$props.id;
            }
        },
        props: ["id", "name"]
    }
</script>
