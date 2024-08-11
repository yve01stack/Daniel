<template>
    <section id="newsletter">
        <div class="newstext">
            <h4>Nouveautés</h4>
            <p>Produits récemment ajoutés et <span> offres spéciales </span>  pour vous. </p>
            <div class="custom-style" v-if="productCategories.length > 0">
              <el-segmented @change="selectCategory" v-model="category" :options="productCategories" />
            </div>
          </div>
    </section>
</template>

<script setup>
  import { computed, ref, defineEmits, onMounted } from 'vue';
  import { useStore } from 'vuex'; 
  
  const store = useStore()
  const emit = defineEmits(['category']);

  const category = ref('')

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

  const selectCategory = () => {
    emit('category', category.value);
  }

  onMounted(() => {

  });
</script>

<style scoped>

#newsletter  {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  background-image: url(https://i.postimg.cc/R0Bs4qqt/b14.png);
    background-repeat: no-repeat;
    background-position: 20% 30%;
  background-color: #041e42;
  margin: 10px 0 10px 0;
  padding: 16px;
}

#newsletter h4{
  color: #fff;
  font-weight: 700;
  font-size: 22px;
}

#newsletter p{
  color: #818ea0;
  font-weight: 600;
  font-size: 14px;
  margin: 0px 0px 5px 0px;
}

#newsletter p span{
  color: #ffbd27;
}

.custom-style {
  width: 100%;
  overflow-x: hidden;
}

.custom-style:hover {
  overflow-x: auto;
}
/* Custom scrollbar styles */
.custom-style::-webkit-scrollbar {
    width: 4px;
    height: 6px;
  }

.custom-style::-webkit-scrollbar-track {
    background: #041e42; 
    border-radius: 10px;
  }

.custom-style::-webkit-scrollbar-thumb {
    background: #888; 
    border-radius: 10px;
  }

.custom-style::-webkit-scrollbar-thumb:hover {
    background: #555; 
  }

.custom-style .el-segmented {
  --el-segmented-item-selected-color: var(--el-text-color-primary);
  --el-segmented-item-selected-bg-color: #ffd100;
  --el-border-radius-base: 16px;
}

</style>