import { createStore } from 'vuex'
import createPersistedState from "vuex-persistedstate";
import auth from './modules/auth';
import product from './modules/product';
import admin from './modules/admin';


export default createStore({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    auth,
    product,
    admin
  },
  plugins: [createPersistedState()]
})
