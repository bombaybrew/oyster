<template>
  <nav class="navbar is-light" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/">Oyster</router-link>
      <a
        id="burger"
        role="button"
        class="navbar-burger"
        aria-label="menu"
        aria-expanded="false"
        data-target="burger"
        v-on:click="showNav = !showNav"
        v-bind:class="{ 'is-active': showNav }"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div id="menu" class="navbar-menu" v-bind:class="{ 'is-active': showNav }">
      <div class="navbar-start">
        <router-link class="navbar-item" to="/demo">Demo</router-link>
        <router-link class="navbar-item" to="/docs">Docs</router-link>
        <router-link class="navbar-item" to="/about">About</router-link>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <a class="button is-primary">
              <strong>Sign up</strong>
            </a>
            <a class="button is-light">
              Log in
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
export default {
  name: "Navbar",
  data: () => ({
    showNav: false,
  }),
  methods: {
    navigateTo: function(path) {
      this.$data.showNav = !this.$data.showNav;
      this.$router.push(path);
    },
  },
};
</script>
