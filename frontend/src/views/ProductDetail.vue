<template>
  <div class="product_view">
    <div class="product_card">
      <div class="product_img">            
        <img :src="currentProduct.imgSrc" :alt="currentProduct.title" class="main_img">
      </div>
      <div class="info">
        <div class="product_title">{{ currentProduct.title }}</div>
        <span class="brand">{{ currentProduct.storeTitle }}</span>
        <span class="star">
          <el-rate
            v-model="currentProduct.rating"
            disabled
            text-color="#ff9900"
          />
        </span>
        <div style="margin-bottom: 6px;">
          <div class="product_desc_sm" v-html="currentProduct.desc"></div>
          
          <a class="display_more_text" 
          style="color: dodgerblue; margin: -3px 0 0 6px; font-weight: 700; cursor: pointer;" 
          v-if="!showFullText" @click="toggleShow">Afficher plus de détails</a>
        </div>

        <Gallery :medias="currentProduct.media" />
        <span class="available">
          Disponible: 
          <el-tag style="margin-right: 5px;"
            v-for="item in currentProduct.available_in"
            :key="item"
            type="info"
            effect="light"
            round
          >
            {{ item }}
          </el-tag>
        </span>
        <span class="price">{{ currentProduct.price }} {{ currentProduct.currency }}</span>
        <el-button-group v-if="isLoggedIn">
          <el-button round  type="primary" @click="add2Cart(currentProduct.id)" style="padding: 5px 8px;">
            <el-icon><ShoppingCart /></el-icon>
          </el-button>
          <el-button round plain type="primary" @click="orderProduct(currentProduct.id)" style="padding: 5px 8px;">Commander</el-button>
        </el-button-group>
        <el-button-group v-else>
          <el-button round type="primary" style="padding: 5px 8px;">
            <router-link :to="{ name: 'signin' }"><el-icon><ShoppingCart /></el-icon></router-link>
          </el-button>
          <el-button round plain type="primary" style="padding: 5px 8px;">
            <router-link :to="{ name: 'signin' }">Commander</router-link>
          </el-button>
        </el-button-group>           
      </div>
    </div>
  </div>

  <div class="product_view" v-if="showFullText">
    <div class="product_desc_lg">
      <span style="font-weight: 700;">Description:</span>
      <div v-html="currentProduct.desc"></div>
    </div>
  </div>
  
  <div class="header_line_title">
    <h3>Produits Qui Pourraient Vous Plaire</h3>
  </div>
  <section class="pro-container">
    <ProductItem 
      v-for="product in relatedProducts"
      :currentProduct="product"
    />
  </section>
</template>
  
<script setup>
  import ProductItem from '../components/ProductItem.vue'
  import Gallery from '../components/TheGallery.vue';
  import { ShoppingCart } from '@element-plus/icons-vue'
  import { ElMessage } from 'element-plus';
  import { ref, computed } from 'vue';
  import { useStore } from 'vuex';
  import { useRoute, useRouter } from 'vue-router';

  const store = useStore();
  const route = useRoute();
  const router = useRouter();

  const isLoggedIn = computed(() => store.getters['auth/isLoggedIn']);
  const products = computed(() => store.getters['product/products']);

  const currentProduct = computed(() => {
    return products.value.find(product => product.id === Number(route.params.id));
  });

  const add2Cart = async (id) => {
    await store.dispatch('product/addToCart', { prodId: id })
      .then(() => {
        console.log("product added to the cart")
      })      
    };

    const orderProduct = async (id) => {
      await store.dispatch('product/orderProduct', { prodId: id })
        .then((data) => {
          if (data.status === 'success') {
            console.log("product ordered")
            ElMessage(data.message)
          } else {
            ElMessage(data.message)
          }
      })      
    };

  // Tokenize Function
  const tokenize = text => {
    return text.toLowerCase().split(/[^a-zA-Z0-9]+/).filter(Boolean);
  };
  // Calculate Score Function
  const calculateScore = (product1, product2) => {
    const titleTokens1 = tokenize(product1.title);
    const titleTokens2 = tokenize(product2.title);

    const titleCommon = titleTokens1.filter(token => titleTokens2.includes(token)).length;

    return titleCommon;
  };
  // Find Related Products Function
  const findRelatedProducts = (productId, products) => {
    const product = products.find(p => p.id === productId);
    if (!product) {
      return [];
    }

    const relatedProducts = products
      .filter(p => p.id !== product.id)
      .map(p => ({
        ...p,
        score: calculateScore(product, p)
      }))
      .sort((a, b) => b.score - a.score);

    return relatedProducts;
  };
  // A simple keyword matching approach
  const relatedProducts = computed(() => {
    const p = findRelatedProducts(Number(route.params.id), products.value);
    return p.slice(0, 10);;
  });

  const showFullText = ref(false);

  const toggleShow = () => {
    showFullText.value = !showFullText.value;
  };

</script>
  
<style scoped>

  .product_view{
    background: rgba(255, 255, 255, 0.5);
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .product_card {
    position: relative;
    display: flex;
    width: 800px;
    height: 500px;
  }

  .product_desc_lg {
    position: relative;
    width: 800px;
    margin-bottom: 10px;
  }

  .product_desc_sm {
      display: none;
  }
  
  .product_card .product_img {
    z-index: 2;
    background: #1d212b;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 45%;
    height: 90%;
    overflow: hidden;
    transform: translateY(25px);
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
  }

  .product_card .product_img .main_img {
    z-index: 2;
    height: 200px;
    width: 100%;
    object-fit: cover;
    left: -50px;
    transition: transform 0.5s ease;
    transform-origin: center center;
  }

  .product_img:hover .main_img {
    cursor: zoom-in; 
    transform-origin: top left;
    animation: pan 3s infinite alternate;
  }

  @keyframes pan {
    0% {
      transform: scale(1.5) translate(0, 0);
    }
    25% {
      transform: scale(1.5) translate(0, -50%);
    }
    50% {
      transform: scale(1.5) translate(-30%, -50%);
    }
    75% {
      transform: scale(1.5) translate(-50%, 0);
    }
    100% {
      transform: scale(1.5) translate(0, 0);
    }
  }

  .product_card .info {
    z-index: 2;
    background: #f7f7f7;
    display: flex;
    flex-direction: column;
    width: 55%;
    height: 100%;
    box-sizing: border-box;
    padding: 20px;
    border-radius: 10px;
  }
  
  .product_card .info .product_title {
    font-size: 16px;
    line-height: 26px;
    font-weight: 700;
    margin: 5px 5px 10px 9px;
  }
  
  .product_card .info .brand {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-left: 10px;
    margin-top: -10px;
  }

  .product_card .info .star {
    margin: -5px 0 0px 8px;
  }
  
  .product_card .info p, .product_card .info .available {
    font-size: 15px;
    margin: 10px;
  }
  
  .product_card .info .price {
    font-size: 30px;
    font-weight: 300;
    margin: -10px 10px 10px 10px;
  }
  
  /* Related products style */
  .pro-container{
    display: flex;
    justify-content: space-between;
    padding-top: 0px;
    flex-wrap: wrap;
    text-align: center;
  }

  .header_line_title {
    margin-top: 10px;
    margin-bottom: 20px;
    border-bottom: 3px solid #088178;
    width: 160px;
    white-space: nowrap;
    overflow: visible;
  }


  @media (max-width: 900px) {
    .pro-container{
      justify-content: center;
    }

    .display_more_text, .product_desc_lg {
      display: none;
    }

    .product_desc_sm {
      display: block;
    }

    .product_card .info .product_title {      
      margin: 5px 5px 10px 5px;
    }
    
    .product_card {
      flex-direction: column;
      width: 550px;
      height: auto;
    }
  
    .product_card .product_img {
      width: 100%;
      height: 200px;
      transform: translateY(0);
      border-bottom-left-radius: 0;
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
    }

    .product_card .product_img img {
      width: 100%;
      height: 100%;
      left: initial;
  }
  
    .product_card .info {
      background-color: #ffffff;
      width: 100%;
      height: auto;
      padding: 20px 0px 0px 0px;
      border-top-left-radius: 0;
      border-top-right-radius: 0;
    }
  
    .product_card .info p, .product_card .info .available {
      margin: 5px;
      font-size: 13px;
    }
  
    .product_card .info .price {
      margin: 5px;
      font-size: 30px;
    }

    .product_card .info .brand {
      margin-left: 5px;
      margin-top: -10px;
    }

    .product_card .info .star {
      margin-left: 2px;
      margin-top: -10px;
    }
  
  }

  @media (max-width: 477px) {
    .product_card .product_img {
      width: 100%;
      height: 200px;
      transform: translateY(0);
      border-bottom-left-radius: 0;
      border-top-left-radius: 0px;
      border-top-right-radius: 0px;
    }

  }
  
</style>
  