<template>
  <div class="card is-4">
    <div class="card-content">
      <p class="title is-4 is-spaced">
        {{ title }}
      </p>
      <p class="subtitle is-6">
        {{ subtitle }}
      </p>
    </div>
    <footer class="card-footer">
      <a href="#" class="card-footer-item">{{ action }}</a>
    </footer>
  </div>
</template>

<script>
export default {
  name: "Card",
  props: ["title", "subtitle", "action"],
};
</script>

<style scoped>

.card-content {
   height: 12rem;
}

</style>