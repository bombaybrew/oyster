<template>
  <nav class="navbar is-light" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item">
        <router-link to="/">Oyster</router-link>
      </a>

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
        <a class="navbar-item">
          <router-link to="/demo">Demo</router-link>
        </a>
        <a class="navbar-item">
          <router-link to="/docs">Docs</router-link>
        </a>
        <a class="navbar-item">
          <router-link to="/about">About</router-link>
        </a>
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
