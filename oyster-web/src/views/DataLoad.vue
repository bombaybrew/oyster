<template>
  <section class="section">
    <div class="content">
      <div class="container">
        <h3>Select Dataset</h3>
        <hr />
        <div class="columns is-mobile">
          <div class="column is-half-mobile is-2-desktop">
            <card
              title="Import CSV"
              subtitle="Import local CSV file"
              action="+ Import Data"
              @click="uploadFile"
            />
          </div>
        </div>
        <div class="columns is-mobile">
          <div
            class="column is-half-mobile is-2-desktop"
            v-for="item of datasets"
            v-bind:key="item"
          >
            <card v-bind:title="item.name" subtitle="" action="Use Dataset" />
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
    navigateTo: function(path) {
      console.log(path);
      this.$router.push(path);
    },
  },
};
</script>
