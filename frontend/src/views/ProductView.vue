<template>
    <ProductFilter 
      :categories="productCategories" 
      :availabilities="countryList" 
      @queryData="handleQuery"/>
    
    <section class="pro-container">
      <ProductItem 
        v-for="product in displayedProducts"
        :currentProduct="product"
      />
    </section>
    <div class="button-container">
      <el-button @click="seeMore" size="large" round :disabled="allProductsDisplayed">Voir Plus+</el-button>
    </div>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue';
  import { useStore } from 'vuex'; 
  import ProductItem from '../components/ProductItem.vue'
  import ProductFilter from '../components/ProductFilter.vue'
  
  const store = useStore()
  
  const products = computed(() => store.getters['product/products']);

  const productCategories = computed(() => {
    // Step 1: Extract unique categories
    const uniqueCategories = [...new Set(products.value.map(product => product.category))];
    // Step 2: Transform into the desired format
    const categoryList = uniqueCategories.map(category => ({
      value: category,
      label: category
    }));
  
    return categoryList;
  });
  
  const countryList = computed(() => {
    // Flatten the available_in arrays into one unique countries array
    const uniqueCountries = [...new Set(products.value.flatMap(product => product.available_in))];
    const countryList = uniqueCountries.map(country => ({
      value: country,
      label: country
    }));
  
    return countryList;
  });
  
  const filterAndSortProducts = (products, filterQuery) => {
    return products.value
      .filter((product) => {
        // Filter by query (title and description)
        const query = filterQuery.query.toLowerCase();
        if (query) {
          const titleMatches = product.title.toLowerCase().includes(query);
          if (!titleMatches) {
            return false;
          }
        }
  
        // Filter by category
        if (filterQuery.category.length && !filterQuery.category.includes(product.category)) {
          return false;
        }
  
        // Filter by availability in countries
        if (filterQuery.available_in.length) {
          const availableInMatch = filterQuery.available_in.some(country => product.available_in.includes(country));
          if (!availableInMatch) {
            return false;
          }
        }
  
        return true;
      })
      .sort((a, b) => {
        // Sort by specified criteria
        if (filterQuery.sortBy === 'price') {
          return a.price - b.price;
        } else if (filterQuery.sortBy === 'rating') {
          return b.rating - a.rating;
        }
        return 0; // No sorting if no valid sortBy value
      });
  };
  
  // See more button
  const productsPerPage = 10;
  const displayedCount = ref(productsPerPage);
  
  let filteredProducts = products.value;
  const handleQuery = (filterQuery) => {
    filteredProducts = filterAndSortProducts(products, filterQuery);
    displayedCount.value = productsPerPage;
    seeMore()
  };
  
  const displayedProducts = computed(() => {
    return filteredProducts.slice(0, displayedCount.value);
  });
  
  const allProductsDisplayed = computed(() => {
    return displayedCount.value >= filteredProducts.length;
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
      justify-content: center
    }
    
  }
  
  </style>