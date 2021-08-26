<template>
  <div class="container">
    <div class="columns is-multiline is-mobile">
      <div
        class="column is-half-mobile is-2-desktop"
        v-for="item of datasets"
        v-bind:key="item"
      >
        <card
          v-bind:title="item.name"
          v-bind:id="item.id"
          subtitle=""
          action="Use Dataset"
          @click="onDatasetSelect(item.id, item.name)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Card from "@/views/components/Card.vue";
export default {
  components: { Card },
  name: "ExistingDataset",
  data() {
    return {
      datasets: [],
    };
  },
  inject: ["$http"],
  created: async function() {
    let result = await this.$http.getAllDatasets();
    this.datasets = result.data;
    console.log(this.datasets)
  },
  methods: {
    onDatasetSelect: function(datasetID, datasetName) {
      console.log(datasetID, datasetName);
      this.$router.push({
        name: "dataset",
        params: {
          "id": datasetID,
          "datasetName": datasetName
        },
      });
    },
  },
};
</script>
