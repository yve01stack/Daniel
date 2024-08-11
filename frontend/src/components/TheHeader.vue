<script setup>
import { RouterLink } from 'vue-router'
import { useStore } from 'vuex';
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus'

const router = useRouter();
const store = useStore();

const isLoggedIn = computed(() => store.getters['auth/isLoggedIn']);
const cartTotal = computed(() => store.getters['product/totalSum']);
const cartProducts = computed(() => store.getters['product/carts']);
const socketCart = computed(() => store.getters['product/quantity']);

const logoutUser = async () => {
  await store.dispatch('auth/logoutUser')
  .then(() => router.push({ name: 'home' }))
};

const fetchCarts = async () => {
  await store.dispatch('product/fetchCarts');
};

const removeFromCart = async (id) => {
  await store.dispatch('product/removeFromCart', { cartId: id });
};

const increaseQuantity = async (id) => {
  await store.dispatch('product/increaseQuantity', { cartId: id })
};

const decreaseQuantity = async (id) => {
  await store.dispatch('product/decreaseQuantity', { cartId: id })
};

// Product cart control
let cartVisible = ref(false)

const cartOpen = () => {
  if (isLoggedIn.value) {
    cartVisible.value = true;
    fetchCarts()
  } else {
    router.push({name: 'signin'});
  }
};

const orderCart = async () => {
  await store.dispatch('product/orderCart')
  .then((data) => {
    ElMessage(data.message)
    cartVisible.value = false;
    router.push({name: 'profile'})
  })
};


// Side menu control
var side_menu_icon = true;

const sideMenu = () => {
  const bar = document.getElementById('bar')
  const close = document.getElementById('close')
  const nav = document.getElementById('navbar')
  
  nav.classList.toggle("active");

  if (side_menu_icon){
    side_menu_icon = false;
    bar.style.display = "none";
    close.style.display = "block";
   } else{
    side_menu_icon = true;
    bar.style.display = "block";
    close.style.display = "none";
  }

};

const fetchProducts = async () => {
  await store.dispatch('product/fetchProducts');
};

onMounted(() => {
  fetchProducts();
});

</script>

<template>
  <header>
    <RouterLink to="/">
        <img src="@/assets/logo_sm.png" class="logo_sm">
    </RouterLink>
    <div>
      <ul id="navbar" @click="sideMenu">
        <li><RouterLink class="active" to="/">Accueil</RouterLink></li>
        <li><RouterLink to="/product/all">Produits</RouterLink></li>
        <li v-if="isLoggedIn"><RouterLink to="/user/profile">Profil</RouterLink></li>
        <li v-if="isLoggedIn"><a @click="logoutUser">Se deconnecter</a></li>
        <li v-else><RouterLink to="/signin">Se connecter</RouterLink></li>
        <li @click="cartOpen" id="lg-bag"><a><i class="fal fa-shopping-bag"></i></a>
          <span class="quantity" v-if="socketCart > 0"> {{ socketCart }}</span>
        </li>
      </ul>
    </div>

    <div id="mobile">
      <a @click="cartOpen"><i class="fal fa-shopping-bag"></i>
        <span class="quantity" v-if="socketCart > 0"> {{ socketCart }}</span>
      </a>
      <a @click="sideMenu">
        <i id="bar" class="fas fa-stream"></i>
        <i id="close" class="far fa-times"></i>
      </a>
    </div>
  </header>

  <!-- Cart modal -->
  <section>
    <el-dialog v-model="cartVisible" width="340">
      <template #header="{titleId, titleClass }">
        <div>
          <h3 :id="titleId" :class="titleClass">Panier d'achat</h3>
        </div>
      </template>
      <div class="cart-container customScrollbar">
        <div class="cart-item" v-for="cart in cartProducts">
          <div class="cart-item-image">
            <router-link :to="{ name: 'product_detail', params: { id: cart.product.id } }">  
              <img :src="cart.product.imgSrc" :alt="cart.product.storeTitle">
            </router-link>
          </div>
          <div class="cart-item-details">
              <h5 class="cart-item-title">{{ cart.product.title }}</h5>
              <div class="cart-item-btn">
                  <button class="quantity-btn" @click="decreaseQuantity(cart.id)">-</button>
                  <input type="number" id="quantity-input" :value="cart.quantity" min="1" readonly>
                  <button class="quantity-btn" @click="increaseQuantity(cart.id)">+</button>
                  <button class="delete-btn" @click="removeFromCart(cart.id)">Supprimer</button>
              </div>
              <div class="total-price">  
                 {{ cart.product.price*cart.quantity }} {{ cart.product.currency }}</div>
          </div>
        </div>
      </div>
      <template #footer>
        <h3>Montant total: {{ cartTotal }} Fcfa</h3>
        <div class="dialog-footer">
          <el-button type="primary" :disabled="socketCart===0" @click="orderCart">Commander</el-button>
        </div>
      </template>
    </el-dialog>
  </section>

</template>

<style scoped>
header{
  position: fixed;
  width: 100%;
  overflow: hidden;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10% 8px 10%;
  background-color: #FFF;
  border-bottom: 1px solid #DCDCDC;
}

#navbar{
  display: flex;
  align-items: center;
  justify-content: center;
}

.quantity{
  background-color: #6394F8;
  border-radius: 50%;
  color: white;
  position: absolute;
  font-size: 8px;
  line-height: 1;
  padding: 3px 5px;
  text-align: center;
  vertical-align: middle;
  white-space: nowrap;
  margin-left: -9px;
  bottom: 0.8rem;
}

#mobile{
  display: none;
  align-items: center;
  cursor: pointer;
}

#navbar li {
  list-style: none; 
  padding: 0 20px;
  position: relative;
}

#navbar li a {
  text-decoration: none;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  transition: 0.5s ease;
  cursor: pointer;
}

#navbar li a:hover,
#navbar li a.active{
  color: #088178;
}

#navbar li a:hover::after,
#navbar li a.active::after{
  content: " ";
  width: 40%;
  height: 2px;
  background: 2px;
  background-color: #088178;
  position: absolute;
  bottom: -4px;
  left: 20px;
}

#navbar #lg-bag a:hover::after {
  content: " ";
  width: 0%;
  height: 0px;
}

.logo_sm {
  height:34px;
}

/* Cart item style */
.cart-container {
  max-height: 320px;
  overflow-y: auto;
  overflow-x: hidden;
}

.cart-item {
    display: flex;
    align-items: center;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 6px;
    margin-bottom: 10px;
    background-color: #f9f9f9;
    height: 88px;
}

.cart-item-image img {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
    margin-top: 6px;
}

.cart-item-details {
    flex-grow: 1;
    padding-left: 10px;
}

.cart-item .cart-item-title {
    /* width: 90%; */
    width: 200px;
    font-size: 14px;
    justify-content: space-between;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.cart-item-btn {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-top: 5px;
}

.cart-item-btn .quantity-btn {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.cart-item-btn .quantity-btn:hover {
    background-color: #2980b9;
}

.cart-item-btn .delete-btn {
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.cart-item-btn .delete-btn:hover {
    background-color: #c0392b;
}
#quantity-input {
    width: 30px;
    text-align: center;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px;
}

/* Chrome, Safari, Edge, Opera */
#quantity-input::-webkit-outer-spin-button,
#quantity-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
#quantity-input {
  -moz-appearance: textfield;
}

.total-price {
    margin-top: 5px;
    font-size: 14px;
    font-weight: bold;
    color: #333;
}

@media (max-width: 920px) {
  
#navbar{
  display: flex;
  flex-direction: column;   
  align-items: flex-start;
  justify-content: flex-start;
  position: fixed;
  top: 58px;
  right: -300px;
  height: 100vh;
  width: 300px;
  background-color: #F8F8F8;
  padding: 8px 0 8px 0;
  transition: 0.3s
}
  
  #navbar.active{
  right: 0;
}

  #navbar li{
    margin-bottom: 25px
  }
  
  #mobile{
    display: flex;
    align-items: center
}
  #mobile i{
    font-size: 18px;
    color: #1a1a1a;
    padding-left: 20px
  }
  
  #close, #lg-bag{
    display: none
  } 
  
  .quantity{
    bottom: 2.15rem;
  }

}

@media (max-width: 477px) {

  .container{
    padding: 90px 5% 5px 5%;
  }

  header{
    padding: 8px 10px 8px 10px;
  }
  
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
}
</style>
