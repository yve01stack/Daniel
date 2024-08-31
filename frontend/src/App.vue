<script setup>
import { RouterView } from 'vue-router'
import TheHeader from './components/TheHeader.vue'
import TheFooter from './components/TheFooter.vue'
</script>

<template>
  <TheHeader />

  <section class="container">
    <RouterView />
  </section>
  
  <TheFooter />
</template>

<style scoped>
.container{
  padding: 90px 15% 10px 15%;
  overflow-x: hidden;
}

@media (max-width: 477px) {
  .container{
    padding: 90px 5% 10px 5%;
  }

}

@media (max-width: 920px) {
  .container{
    padding: 90px 10% 10px 10%;
  }

}

</style>
