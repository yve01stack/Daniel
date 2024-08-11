import { service } from '@/api'

const namespaced = true;

const state = {
  orders: [],
  dashboard: {},
  categories: [],
  searchItems: [],
  item: null,
};

const getters = {
  orders: state => state.orders,
  dashboard: state => state.dashboard,
  categories: state => state.categories,
  searchItems: state => state.searchItems,
  item: state => state.item,
};

const actions = {

  async fetchOrders({ commit }) {
    const response = await service.get('/admin/order/fetch')
    if (response['data'].status==="success") {
      await commit('setOrders', response.data['orders']);
    }
    return response['data'];
  },

  async removeOrder({ commit }, orderId) {
    const response = await service.post('/admin/order/remove', orderId) 
    if (response['data'].status==="success") {
      await commit('setOrders', response.data.orders);
    }
    return response['data'];
  },

  async cancelOrder({ commit }, orderId) {
    const response = await service.post('/admin/order/cancel', orderId) 
    if (response['data'].status==="success") {
      await commit('setOrders', response.data.orders);
    }
    return response['data'];
  },

  async confirmProof({ commit }, form) {
    const response = await service.post('/admin/order/confirm_paid', form) 
    if (response['data'].status==="success") {
      await commit('setOrders', response.data.orders);
    }
    return response['data'];
  },

  async orderDelivery({ commit }, form) {
    const response = await service.post('/admin/order/delivery', form) 
    if (response['data'].status==="success") {
      await commit('setOrders', response.data.orders);
    }
    return response['data'];
  },

  async aliCategory({ commit }) {
    const response = await service.get('/admin/aliexpress/categories') 
    if (response['data'].status==="success") {
      
      let rawData = response.data.categories;
      let categories = [];

      rawData.forEach(element => {
        if (element.name !== null) {
          
          let cleanItems = [];
          element.list.forEach(item => {
            if (item.name !== null) {
              cleanItems.push(item);
            }
          })
          element.list = cleanItems;
          categories.push(element);
        }
      })
      await commit('setCategories', categories);
    }
    return response['data'];
  },

  async aliSearch({ commit }, form) {
    const response = await service.post('/admin/aliexpress/search', form) 
    if (response['data'].status==="success") {
      await commit('setSearchItems', response.data.searchItems);
    }
    return response['data'];
  },

  async aliProduct({ commit }, form) {
    const response = await service.post('/admin/aliexpress/item', form) 
    if (response['data'].status==="success") {
      await commit('setItem', response.data.item);
    }
    return response['data'];
  },

  async addProduct({ commit }, form) {
    const response = await service.post('/admin/product/add', form) 
    return response['data'];
  },

  async updateProduct({ commit }, form) {
    const response = await service.post('/admin/product/update', form) 
    return response['data'];
  },

  async fetchDashboard({ commit }) {
    const response = await service.get('/admin/dashboard')
    if (response['data'].status==="success") {
      await commit('setDashboard', response.data['dashboard']);
    }
    return response['data'];
  },


  
};

    
const mutations = {

  setOrders(state, orders) {
    state.orders = orders;
  },

  setCategories(state, categories) {
    state.categories = categories;
  },

  setSearchItems(state, searchItems) {
    state.searchItems = searchItems;
  },

  setItem(state, item) {
    state.item = item;
  },

  setDashboard(state, dashboard) {
    state.dashboard = dashboard;
  },

  logoutUserState(state) {
    state.orders = [];
    state.categories = [];
    state.searchItems = [];
    state.item = null;
    state.dashboard = {}
  }
  
};

export default {
  namespaced,
  state,
  getters,
  actions,
  mutations
};