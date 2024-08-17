<template>
    <section id="newsletter">
        <div class="newstext">
            <h4>Nouveautés</h4>
            <p>Produits récemment ajoutés et <span> offres spéciales </span>  pour vous. </p>
            
            <div class="slider-container" v-if="productCategories.length > 0">
              <el-button style="margin-right: 10px; background-color: rgba(255, 255, 255, 0);" circle @click="scrollLeft" :icon="ArrowLeft" />
              <div class="slider" ref="slider">
                <div
                  v-for="category in productCategories"
                  :class="['category', { selected: category === selectedCategory }]"
                  @click="selectCategory(category)"
                >
                  {{ category }}
                </div>
              </div>
              <el-button style="margin-left: 10px; background-color: rgba(255, 255, 255, 0);" circle @click="scrollRight" :icon="ArrowRight" />
            </div>

          </div>
    </section>

</template>

<script setup>
  import { computed, ref, defineEmits, onMounted } from 'vue';
  import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
  import { useStore } from 'vuex'; 
  
  const store = useStore()
  const emit = defineEmits(['category']);

  const category = ref('')

  const products = computed(() => store.getters['product/products']);
  
  const productCategories = computed(() => {
    // Extract unique categories
    const uniqueCategories = [...new Set(products.value.map(product => product.category))];

    return uniqueCategories;
  });

const selectedCategory = ref(null);
const slider = ref(null);

function selectCategory(category) {
  selectedCategory.value = category;
  emit('category', category);
}

const scrollLeft = () => {
  if (slider.value) {
    slider.value.scrollBy({ left: -200, behavior: 'smooth' });
  }
}

const scrollRight = () => {
  if (slider.value) {
    slider.value.scrollBy({ left: 200, behavior: 'smooth' });
  }
}

</script>

<style scoped>

#newsletter  {
  /* display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap; */
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

/* Categories slider */
.slider-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
}

.slider-container .slider {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  white-space: nowrap;
  scroll-behavior: smooth;
  flex: 1;
}

.slider-container .slider::-webkit-scrollbar {
  width: 0px;
  height: 0px;
}

.slider-container .slider .category {
  padding: 3px 6px;
  border-radius: 10px;
  background-color: #f1f1f150;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
  font-weight: 500;
  color: whitesmoke;
}

.slider-container .slider .category:hover {
  background-color:  #f1f1f170;
}

.slider-container .slider .selected {
  background-color:  #f1f1f180;
}

</style>
