<template>
  <div>
    <Navbar></Navbar>
    <router-view></router-view>
    <Footer></Footer>
  </div>
</template>

<script>
import Navbar from "@/views/components/Navbar";
import Footer from "@/views/components/Footer.vue";

export default {
  name: "App",
  components: {
    Navbar,
    Footer,
  },
};
</script>

<style>
@import "./assets/oyster.css";
</style>
