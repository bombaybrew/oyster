<template>
  <section class="section">
    <div class="content">
      <div class="container">
        <div class="columns is-mobile">
          <div class="column is-half-mobile is-2-desktop">
            <card
              title="Import CSV"
              subtitle="Import local CSV file"
              action="+ Import Data"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Card from "@/views/components/Card.vue";
export default {
  components: { Card },
  name: "DataLoad",
  methods: {
    navigateTo: function(path) {
      console.log(path);
      this.$router.push(path);
    },
  },
};
</script>
