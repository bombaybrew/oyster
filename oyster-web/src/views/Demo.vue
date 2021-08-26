<template>
  <section class="section">
    <div class="content">
      <div class="container">
        <h1>Demo</h1>
        <hr />

        <form id="demoForm" @submit.prevent="processForm">
          <div class="field">
            <label class="label">Model</label>
            <div class="control">
              <model-dropdown
                v-bind:title="dropdownTitle"
                v-bind:models="models"
                v-on:onSelect="onModelSelect"
              ></model-dropdown>
            </div>
          </div>

          <div class="field">
            <label class="label">Test Data</label>
            <div class="control">
              <textarea
                class="textarea"
                placeholder="Test Data"
                v-model="testText"
              ></textarea>
            </div>
          </div>

          <div class="field is-grouped">
            <div class="control">
              <button type="submit" class="button is-link">Test</button>
            </div>
            <div class="control">
              <button class="button is-link is-light">Reset</button>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <textarea
                class="textarea"
                placeholder=""
                v-model="modelTestResult"
                readonly
              ></textarea>
            </div>
          </div>
        </form>
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
    selectedModel: {},
    models: [],
    testText: "",
    modelTestResult: "",
  }),
  mounted() {
    this.initDemo();
  },
  inject: ["$http"],
  methods: {
    initDemo: async function() {
      try {
        let result = await this.$http.getDemoModels();
        this.models = result.data.data;
        console.log(this.models);
      } catch (e) {
        console.log(e);
      }
    },
    onModelSelect: async function(selected) {
      await this.$nextTick();
      this.dropdownTitle = selected.name;
      this.selectedModel = selected;
    },
    processForm: async function() {
      try {
        let result = await this.$http.testModel(
          this.selectedModel.id,
          this.testText
        );
        console.log(result.data);
        this.modelTestResult = result.data;
      } catch (e) {
        console.log(e);
      }
    },
  },
};
</script>
