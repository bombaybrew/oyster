<template>
  <section class="section">
    <div class="content">
      <div class="container">
        <div class="tabs">
          <ul>
            <li v-bind:class="{ 'is-active': activeTab == 'home_tab' }">
              <a v-on:click="activeTab = 'home_tab'">Home</a>
            </li>
            <li v-bind:class="{ 'is-active': activeTab == 'library_tab' }">
              <a v-on:click="activeTab = 'library_tab'">Library</a>
            </li>
            <li v-bind:class="{ 'is-active': activeTab == 'setting_tab' }">
              <a v-on:click="activeTab = 'setting_tab'">Setting</a>
            </li>
          </ul>
        </div>
        <div class="tab-contents">
          <div
            class="content"
            v-bind:class="{ 'is-active': activeTab == 'home_tab' }"
          >
            Home
          </div>
          <div
            class="content"
            v-bind:class="{ 'is-active': activeTab == 'library_tab' }"
          >
            Library
          </div>
          <div
            class="content"
            v-bind:class="{ 'is-active': activeTab == 'setting_tab' }"
          >
            Setting
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "Home",
  data: () => ({
    activeTab: "home_tab",
  }),
};
</script>
