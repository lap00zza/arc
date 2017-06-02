<template>
    <div class="flex-column flex-spacer login__view">
        <div class="title-bar">
            <span class="title">arc!</span>&nbsp;<span class="subtitle">dead simple chat</span>
        </div>
        <div class="server-info">
            <div class="name">Log in to arc!</div>
            <div class="description">may the force be with you</div>
            <div id="notification">{{ status }}</div>
            <form v-on:submit="onSubmit">
                <input v-model="email" type="text" placeholder="email" required>
                <input v-model="password" type="password" placeholder="password" required>
                <button type="submit" v-bind:class="in_progress ? 'login__btn--in-progress' : 'login__btn--rest'">
                    <span>Log in</span>
                    <img src="/assets/images/puff.svg">
                </button>
            </form>
            <div class="keep-left extras">
                Don't have an account? <router-link to="register">Register</router-link>
            </div>
        </div>
        <div class="login__meta">
            Did you know you can host your very own arc! server?
            <a href="https://github.com/lap00zza/arc" target="_blank">Find out how.</a>
        </div>
    </div>
</template>
<script src="./loginView.js"></script>
