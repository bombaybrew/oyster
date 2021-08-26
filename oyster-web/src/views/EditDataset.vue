<template>
  <section class="section">
    <div class="content">
      <div class="container">
        <h2>{{ datasetName }}</h2>

        <table class="table is-hoverable is-striped">
          <tbody>
            <tr v-for="row in rows" :key="row.id">
              <td>{{ row.data }}</td>
            </tr>
          </tbody>
        </table>
        <nav class="pagination" role="navigation" aria-label="pagination">
          <a class="pagination-previous">Previous</a>
          <a class="pagination-next">Next page</a>
        </nav>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  components: {},
  name: "EditDataset",
  props: ["id", "datasetName"],
  inject: ["$http"],
  data() {
    return {
      rows: [],
    };
  },
  created: async function() {
    console.log("oncreated - ", this.id, this.datasetName);
    let result = await this.$http.getDatasetRows(this.id);
    this.rows = result.data.data;
  },
  methods: {
    navigateTo: function(path) {
      console.log(path);
      this.$router.push("/create");
    },
  },
};
</script>
