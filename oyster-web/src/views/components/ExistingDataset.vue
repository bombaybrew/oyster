<template>
  <div class="container">
    <div class="columns is-multiline is-mobile">
      <div
        class="column is-half-mobile is-2-desktop"
        v-for="item of datasets"
        v-bind:key="item"
      >
        <card v-bind:title="item.name" subtitle="" action="Use Dataset" />

        <!-- <card
          title="Create Model"
          subtitle="Text classfication, entity extraction"
          action="+ Create Model"
          @click="selectDataset('/create')"
        /> -->
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
  },
  methods: {
    selectDataset: function(path) {
      console.log(path);
      this.$router.push("/create");
    },
  },
};
</script>
