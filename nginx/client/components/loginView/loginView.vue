<template>
    <div class="flex-column flex-spacer login-view">
        <div class="title-bar">
            <span class="title">arc!</span>&nbsp;<span class="subtitle">dead simple chat</span>
        </div>
        <div class="server-info">
            <div class="name">Log in to <span>{{ serverName }}</span></div>
            <div class="description">{{ serverDesc }}</div>
            <form v-on:submit="onSubmit">
                <input name="email" type="text" placeholder="email">
                <input name="password" type="password" placeholder="password">
                <button type="submit">Log in</button>
            </form>
            <div class="keep-left extras">
                <a href="#" id="register">Register</a>
                <a href="#" id="guest_login" class="pull-right">Continue as Guest</a>
            </div>
        </div>
        <div class="_login_meta">
            Did you know you can host your very own arc! server?
            <a href="https://github.com/lap00zza/arc" target="_blank">Find out how.</a>
        </div>
    </div>
</template>
<script src="./loginView.js"></script>
