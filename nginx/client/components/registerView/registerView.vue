<template>
    <div class="flex-column flex-spacer login__view">
        <div class="title-bar">
            <span class="title">arc!</span>&nbsp;<span class="subtitle">dead simple chat</span>
        </div>
        <div class="server-info">
            <div class="name">Register</div>
            <div class="description">and get ready to experience awesomeness</div>
            <div id="notification">{{ status }}</div>
            <form v-on:submit="onSubmit">
                <input v-model="username" type="text" placeholder="username" required>
                <input v-model="email" type="text" placeholder="email" required>
                <input v-model="password" type="password" placeholder="password" required>
                <button type="submit" v-bind:class="in_progress ? 'login__btn--in-progress' : 'login__btn--rest'">
                    <span>Register</span>
                    <img src="/assets/images/puff.svg">
                </button>
            </form>
            <div class="keep-left extras">
                Already have an account? <router-link to="login">Login</router-link>
            </div>
        </div>
        <div class="login__meta">
            Did you know you can host your very own arc! server?
            <a href="https://github.com/lap00zza/arc" target="_blank">Find out how.</a>
        </div>
    </div>
</template>
<script src="./registerView.js"></script>
