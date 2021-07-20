<template>
  <footer class="footer">
    <div class="container">
      <div class="content">
        <div class="columns">
          <div class="column is-3">
            <p>
              <router-link to="/">Home</router-link>
            </p>
            <p>
              <router-link to="/docs">Docs</router-link>
            </p>
            <p>
              <router-link to="/about">About</router-link>
            </p>
          </div>
        </div>
      </div>
      <p><strong>Oyster</strong> 2021</p>
    </div>
  </footer>
</template>
<script>
export default {
  name: "Footer",
};
</script>
