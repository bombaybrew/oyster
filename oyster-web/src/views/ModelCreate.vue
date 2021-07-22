<template>
  <section class="section">
    <div class="content">
      <div class="container">
        <h3>Select Model Type</h3>
        <hr />
        <div class="columns is-mobile">
          <div class="column is-half-mobile is-2-desktop">
            <card
              title="Entity Extraction"
              subtitle="Identify key elements from text, and classify into pre-defined tags"
              action="+ Create Model"
              @click="navigateTo('/dataload')"
            />
          </div>
          <div class="column is-half-mobile is-2-desktop">
            <card
              title="Text Classifier"
              subtitle="Classify text into pre-defined tags"
              action="+ Create Model"
              @click="navigateTo('/dataload')"
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
  name: "ModelCreate",
  methods: {
    navigateTo: function(path) {
      console.log(path);
      this.$router.push(path);
    },
  },
};
</script>
