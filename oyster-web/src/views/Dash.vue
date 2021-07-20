<template>
  <div class="container">
    <div class="columns is-mobile">
      <div class="column is-half-mobile is-2-desktop">
        <card
          title="Create Model"
          subtitle="Text classfication, entity extraction"
          action="+ Create Model"
        />
      </div>
    </div>
    <h3>Existing Models</h3>
    <hr />
  </div>
</template>

<script>
import Card from "@/views/components/Card.vue";
export default {
  components: { Card },
  name: "Dash",
};
</script>
