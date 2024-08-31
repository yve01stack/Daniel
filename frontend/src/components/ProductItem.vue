<script setup>
import { defineProps, computed } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

const store = useStore();
const route = useRoute();

const props = defineProps({
    currentProduct: { type: Object, required: true },
});

const isLoggedIn = computed(() => store.getters['auth/isLoggedIn']);

const add2Cart = async (id) => {
  if (isLoggedIn) {
    await store.dispatch('product/addToCart', {prodId: id})
    .then(() => {
      console.log("product added to the cart")
    })
  } else {
    route.push({name: 'signin'})
  }
};


</script>

<template>
  <div class="pro">
    <router-link :to="{ name: 'product_detail', params: { id: currentProduct.id } }">  
    <img :src="currentProduct.imgSrc" :alt="currentProduct.category +' '+ currentProduct.storeTitle">
      <div class="des">
        <div class="brand">{{ currentProduct.storeTitle.toLowerCase() }}</div>
        <h5>{{ currentProduct.title }}</h5>
        <div class="star">
          <el-rate
            v-model="currentProduct.rating"
            disabled
            text-color="#ff9900"
          />
        </div>
        <h4>{{ currentProduct.price }} {{ currentProduct.currency }}</h4>
      </div>
    </router-link>
    <a v-if="isLoggedIn" @click="add2Cart(currentProduct.id)"><i class="fal fa-shopping-cart cart"></i></a>
    <a v-else >
      <router-link :to="{ name: 'signin' }">  
        <i class="fal fa-shopping-cart cart"></i>
      </router-link>
    </a>
  </div>
</template>

<style scoped>

.pro{
  width: 19%;
  min-width: 200px;
  padding: 5px 6px;
  border: 1px solid #cce7d0;
  border-radius: 25px;
  cursor: pointer;
  box-shadow: 20px 20px 30px rgba(0, 0, 0, 0.02);
  margin: 10px 0;
  transition: 0.2s ease;
  position: relative;
}

.pro:hover{
   box-shadow: 20px 20px 30px rgba(0, 0, 0, 0.06);
}

.pro img{
  width: 100%;
  border-radius: 20px;
  height: 168px;
}

.pro .des{
  text-align: start;
  padding: 0px 0;
}

.pro .des .brand {
  color: #606063;
  font-size: 12px;
  margin-bottom: -5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pro .des h5{
  padding-top: 5px;
  margin-top: -10px;
  color: #1a1a1a;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

:deep(.el-rate) {
  margin-top: -8px;
  margin-bottom: -8px;
}

:deep(.el-rate__item) {
  margin-right: -8px;
} 
.pro .des h4{
  font-size: 14px;
  padding-top: 5px;
  font-weight: 600;
  color: #088178;
  margin-top: -8px;
}

.pro .cart{
  cursor: pointer;
  width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 50px;
  background-color: #e8f6ea;
  font-weight: 500;
  color: #088178;
  border: 1px solid #cce7d0;
  position: absolute;
  bottom: 9px;
  right: 10px;
  
}

@media (max-width: 1080px) {
  h2 {
    font-size: 30px
  }
  
  h1{
    font-size: 28px
  }
  
  p{
    line-height: 24px;
    font-size: 10px;
  }

  .pro{
    width: 28%;
    min-width: 90px;
    padding: 5px 6px;
    border: 1px solid #cce7d0;
    border-radius: 25px;
    cursor: pointer;
    box-shadow: 20px 20px 30px rgba(0, 0, 0, 0.02);
    margin: 4px;
    transition: 0.2s ease;
    position: relative;
  }

  .pro img {
    height: 150px;
  }
 
}

@media (max-width: 630px) {

 .pro{
    width: 45%;
    margin: 6px;
  }

  .pro img {
    height: 160px;
  }
  
}

@media (max-width: 477px) {
 
  h2 {
    font-size: 30px
  }
  
  h1{
    font-size: 28px
  }
  
  p{
    line-height: 24px;
    font-size: 10px;
  }
  
  .pro{
    width: 45%;
    min-width: 90px;
    padding: 5px 6px;
    border: 1px solid #cce7d0;
    border-radius: 25px;
    cursor: pointer;
    box-shadow: 20px 20px 30px rgba(0, 0, 0, 0.02);
    margin: 4px;
    transition: 0.2s ease;
    position: relative;
  }

  .pro img {
    height: 140px;
  }
  
}
</style>


