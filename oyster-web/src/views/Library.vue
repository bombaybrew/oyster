<template>
  <div class="container">
    <div class="columns is-mobile">
      <div class="column is-half-mobile is-2-desktop">
        <card
          title="Create Model"
          subtitle="Text classfication, entity extraction"
          action="+ Create Model"
          @click="navigateTo('/create')"
        />
      </div>
    </div>
    <hr />
    <h4>Existing DataSets</h4>
    <existing-dataset />
  </div>
</template>

<script>
import Card from "@/views/components/Card.vue";
import ExistingDataset from "@/views/components/ExistingDataset.vue";
export default {
  components: { Card, ExistingDataset },
  name: "Library",
  methods: {
    navigateTo: function(path) {
      console.log(path);
      this.$router.push("/create");
    },
  },
};
</script>
