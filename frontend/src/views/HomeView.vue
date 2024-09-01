<template>
  <HomeBanner />
  
  <section class="pro-container">
    <ProductItem 
      v-for="product in displayedProducts"
      :currentProduct="product"
    />
  </section>
  <div class="button-container" v-if="!allProductsDisplayed">
    <el-button @click="seeMore" size="large" round :disabled="allProductsDisplayed">Voir Plus+</el-button>
  </div>

  <ProductBanner @category="handleCategory" />

  <section class="pro-container">
    <ProductItem 
      v-for="product in categoryProducts"
      :currentProduct="product"
    />
  </section>
  
</template>

<script setup>
import { computed, ref } from 'vue';
import { useStore } from 'vuex'; 
import ProductItem from '../components/ProductItem.vue'
import HomeBanner from '../components/HomeBanner.vue'
import ProductBanner from '../components/ProductBanner.vue'

const store = useStore()

const products = computed(() => store.getters['product/products']);

const selectedCategory = ref('');
const handleCategory = (category) => {
  selectedCategory.value = category;
};

const categoryProducts = computed(() => {
  if (!selectedCategory.value) {
    return products.value.slice(0, 20);
  }
  return products.value.filter(product => product.category === selectedCategory.value).slice(0, 20);
});

// See more button
const productsPerPage = 10;
const displayedCount = ref(productsPerPage);

const displayedProducts = computed(() => {
  return products.value.slice(0, displayedCount.value);
});

const allProductsDisplayed = computed(() => {
  return displayedCount.value >= products.value.length;
});

const seeMore = () => {
  displayedCount.value += productsPerPage;
};

</script>

<style scoped>
.pro-container{
  display: flex;
  justify-content: space-between;
  padding-top: 0px;
  flex-wrap: wrap;
  text-align: center;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

@media (max-width: 920px) {
  .pro-container{
    /* justify-content: space-between; */
    justify-content: center
  }
  
}

</style>