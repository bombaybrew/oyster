<template>
  <div class="content">
    <div class="dropdown" v-bind:class="{ 'is-active': showDropdownMenu }">
      <div
        class="dropdown-trigger"
        v-on:click="showDropdownMenu = !showDropdownMenu"
      >
        <button
          class="button"
          aria-haspopup="true"
          aria-controls="dropdown-menu"
        >
          <span>{{ title }}</span>
          <span class="icon is-small">
            <i class="fas fa-angle-down" aria-hidden="true"></i>
          </span>
        </button>
      </div>
      <div class="dropdown-menu" id="dropdown-menu" role="menu">
        <div class="dropdown-content">
          <a
            class="dropdown-item"
            v-for="model in models"
            v-bind:key="model.id"
            @click="onSelect(model)"
          >
            {{ model.name }}
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ModelDropdown",
  props: ["title", "models"],
  data: () => ({
    showDropdownMenu: false,
  }),
  methods: {
    onSelect: function(model) {
      console.log("model - ", model.name);
      this.showDropdownMenu = !this.showDropdownMenu;
      this.$emit("onSelect", model);
    },
  },
};
</script>
