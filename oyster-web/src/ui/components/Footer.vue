<template>
  <footer class="footer">
    <div class="container">
      <div class="content">
        <div class="columns">
          <div class="control">
            <b-navbar-item
              class="has-text-weight-semibold"
              tag="router-link"
              :to="{ path: '/' }"
            >
              Home
            </b-navbar-item>
            <b-navbar-item
              class="has-text-weight-semibold"
              tag="router-link"
              :to="{ path: '/market' }"
            >
              Market
            </b-navbar-item>
            <b-navbar-item
              class="has-text-weight-semibold"
                tag="router-link"
              :to="{ path: '/portfolio' }"
            >
              Portfolio
            </b-navbar-item>
            <b-navbar-item
              class="has-text-weight-semibold"
              tag="router-link"
              :to="{ path: '/about' }"
            >
              About
            </b-navbar-item>
            <p><strong>Oyster</strong> 2021</p>
          </div>
        </div> 
      </div>
    </div>
  </footer>
</template>
<script>
export default {
  name: "Footer"
};
</script>
