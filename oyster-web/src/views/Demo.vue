<template>
  <section class="section">
    <div class="content">
      <div class="container">
        <h1>Demo</h1>
        <hr />
        <model-dropdown
          v-bind:title="dropdownTitle"
          v-bind:models="models"
          v-on:onSelect="onModelSelect"
        ></model-dropdown>
      </div>
    </div>
  </section>
</template>

<script>
import ModelDropdown from "@/views/components/ModelDropdown.vue";
export default {
  components: { ModelDropdown },
  name: "Demo",
  data: () => ({
    dropdownTitle: "Select Model",
    models: [
      {
        id: "724b09e6-89b3-4c4d-a0f0-6148e9984929",
        name: "flair-model",
        type: "NER",
        support: "FLAIR",
        rawDatasetId: "b7e037f2-e999-4a23-bf63-9cbba3a744ae",
        progress: 0,
        processedDatasetId: "cadba24f-648a-4e42-bc7b-c4722e979165",
      },
      {
        id: "df59896f-31f3-4f2a-96fc-c7c6b0e9a334",
        name: "flair-model-classifier",
        type: "CLASSIFIER",
        support: "FLAIR",
        rawDatasetId: "b7e037f2-e999-4a23-bf63-9cbba3a744ae",
        progress: 0,
        processedDatasetId: "cb91f09e-38e9-463e-a0c7-dddf77994f20",
      },
    ],
  }),
  methods: {
    onModelSelect: async function(selected) {
      await this.$nextTick();
      this.dropdownTitle = selected.name;
    },
  },
};
</script>
