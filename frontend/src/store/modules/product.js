import { service } from '@/api'

const namespaced = true;

const state = {
  carts: [],
  total: 0,
  quantity: 0,
  products: [],
  orders: [],
  categories: [],
  availabilities: [],
};

const getters = {
  products: state => state.products,
  totalSum: state => state.total,
  quantity: state => state.quantity,
  carts: state => state.carts,
  orders: state => state.orders,
  categories: state => state.categories,
  availabilities: state => state.countries,
};

const actions = {
  async fetchProducts({ commit }) {
    const response = await service.get('/product/fetch_products')

    await commit('setProducts', response.data['products']);
    await commit('setAvailabilities', response.data['countries']);
    await commit('setCategories', response.data['categories']);
  },

  async fetchCarts({ commit }) {
    const response = await service.get('/product/fetch_carts') 
    if (response['data'].status==="success") {
      await commit("setCarts", response['data'].carts);
    }
    return response['data'];
  },

  async addToCart({ commit }, prodId) {
    const response = await service.post('/product/add_to_cart', prodId)
    if (response['data'].status==="success") {
      await commit("setCarts", response['data'].carts);
    }
    return response['data'];
  },

  async removeFromCart({ commit }, cartId) {
    const response = await service.post('/product/remove_from_cart', cartId) 
    if (response['data'].status==="success") {
      await commit("setCarts", response['data'].carts);
    }
    return response['data'];
  },

  async increaseQuantity({ commit }, cartId) {
    const response = await service.post('/product/increase_qty', cartId)
    if (response['data'].status==="success") {
      await commit("setCarts", response['data'].carts);
    }
    return response['data'];
  },

  async decreaseQuantity({ commit }, cartId) {
    const response = await service.post('/product/decrease_qty', cartId)
    if (response['data'].status==="success") {
      await commit("setCarts", response['data'].carts);
    }
    return response['data'];
  },

  async fetchOrders({ commit }) {
    const response = await service.get('/product/order/fetch')
    if (response['data'].status==="success") {
      await commit('setOrders', response.data['orders']);
    }
    return response['data'];
  },

  async orderCart({ commit }) {
    // Make the request
    try {
      const response = await service.get('/product/order/cart');
      // Check the response status
      if (response.data.status === "success") {
        await commit('setOrders', response.data.orders);
        await commit('setCarts', response.data.carts);
      }
      return response.data;
    } catch (error) {
      // Handle potential errors
      console.error('Error while ordering cart:', error);
      throw error;
    }
  },

  async orderProduct({ commit }, prodId) {
    try {
      const response = await service.post('/product/order/product', prodId);
      // Check the response status
      if (response.data.status === "success") {
        await commit('setOrders', response.data.orders);
        await commit('setCarts', response.data.carts);
      }
      return response.data;
    } catch (error) {
      // Handle potential errors
      console.error('Error while ordering product:', error);
      throw error;
    }
  },

  async removeOrder({ commit }, orderId) {
    const response = await service.post('/product/order/remove', orderId) 
    if (response['data'].status==="success") {
      await commit('setOrders', response.data.orders);
      await commit('setCarts', response.data.carts);
    }
    return response['data'];
  },

  async removeFromOrder({ commit }, orderItemId) {
    const response = await service.post('/product/order/remove_from_order', orderItemId) 
    if (response['data'].status==="success") {
      await commit('setOrders', response.data.orders);
      await commit('setCarts', response.data.carts);    
    }
    return response['data'];
  },

  async increaseOrderItemQuantity({ commit }, orderItemId) {
    const response = await service.post('/product/order/increase_qty', orderItemId)
    if (response['data'].status==="success") {
      await commit('setOrders', response.data.orders);
      await commit('setCarts', response.data.carts); 
    }
    return response['data'];
  },

  async decreaseOrderItemQuantity({ commit }, orderItemId) {
    const response = await service.post('/product/order/decrease_qty', orderItemId)
    if (response['data'].status==="success") {
      await commit('setOrders', response.data.orders);
      await commit('setCarts', response.data.carts); 
    }
    return response['data'];
  },

  async paidProofOrder({ commit }, formData) {
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    const response = await service.post('/product/order/paid', formData, config)
    if (response['data'].status==="success") {
      await commit('setOrders', response.data.orders);
      await commit('setCarts', response.data.carts); 
    }
    return response['data'];
  },

};

    
const mutations = {
  setProducts(state, products) {
    state.products = products.sort((a, b) => new Date(b['created_on']) - new Date(a['created_on']));
  },

  setCarts(state, carts) {
    state.carts = carts;

    let quantity = 0;
    let total = 0;
    carts.forEach(element => {
      quantity += element.quantity;
      total += (element.product.price)*(element.quantity);
    });

    state.quantity = quantity;
    state.total = total;
  },

  setOrders(state, orders) {
    state.orders = orders;
  },

  setCategories(state, categories) {
    state.categories = categories;
  },

  setAvailabilities(state, countries) {
    state.countries = countries;
  },

  logoutUserState(state) {
    state.quantity = 0;
    state.total = 0;
    state.carts = [];
    state.orders = [];
    state.countries = [];
    state.categories = [];
  }
  
};

export default {
  namespaced,
  state,
  getters,
  actions,
  mutations
};