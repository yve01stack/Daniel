import { service } from '@/api'

const namespaced = true;

const state = {
  token: null,
  refresh_token: null,
  user: {},
};

const getters = {
  isLoggedIn: state => !!state.token,
  isModerator: state => state.user && (state.user.status === 'moderator' || state.user.status === 'admin'),
  isAdmin: state => state.user && state.user.status === 'admin',

  StateToken: state => state.token,
  StateRefreshToken: state => state.refresh_token,
  user: state => state.user
};

const actions = {
  async registerUser({ commit }, user) {
    const response = await service.post('/auth/signup', user)
    if (response['data'].status==="success") {
      await commit('setToken', response.data['access_token'], response.data['refresh_token'])
      await commit('setUser', response.data['user_info'])
    } 
    return response['data']   
  },

  async loginUser({ commit }, user) {
    const response = await service.post('/auth/signin', user)
    if (response['data'].status==="success") {
      await commit('setToken', response.data['access_token'], response.data['refresh_token'])
      await commit('setUser', response.data['user_info'])
    } 
    return response['data']    
  },

  async fetchUser({ commit }) {
    const response = await service.get('/auth/user')
    if (response['data'].status==="success") {
      await commit('setToken', response.data['access_token'], response.data['refresh_token'])
      await commit('setUser', response.data['user_info'])
    } 
    return response['data']    
  },

  async logoutUser({ commit }) {
    const response = await service.get('/auth/logout'); 
    if (response['data'].status==="success") {
      await commit('logoutUserState');    
    } 
    return response['data']   
  },

  async edictEmail({ commit }, form) {
    const response = await service.post('/auth/edict_email', form)
    if (response['data'].status==="success") {      
      await commit('setUser', response.data['user_info'])
    } 
    return response['data']    
  },

  async changePwd({ commit }, form) {
    const response = await service.post('/auth/change_pwd', form)
    if (response['data'].status==="success") {
      await commit('setUser', response.data['user_info'])
    } 
    return response['data']    
  },

  async checkEmail({}, form) {
    const response = await service.post('/auth/check_email', form)
    return response['data']    
  },

  async checkedEmail({ commit }, form) {
    const response = await service.post('/auth/checked_email', form)
    if (response['data'].status==="success") {
      await commit('setUser', response.data['user_info'])
    } 
    return response['data']    
  },

  async forgotPassword({ commit }, form) {
    const response = await service.post('/auth/forgot_password', form)
    if (response['data'].status==="success") {
      await commit('setUser', response.data['user_info'])
    } 
    return response['data']    
  },

  async resetPassword({ commit }, form) {
    const response = await service.post('/auth/reset_password', form)
    if (response['data'].status==="success") {
      await commit('setToken', response.data['access_token'], response.data['refresh_token'])
      await commit('setUser', response.data['user_info'])
    } 
    return response['data']    
  },

};

const mutations = {
  setUser(state, user) {
    state.user = user;
  },
  setToken(state, token, refresh_token){
    state.token = token;
    state.refresh_token = refresh_token;
  },
  logoutUserState(state) {
    state.token = null;
    state.refresh_token = null;
    state.user = {};
  }
};

export default {
  namespaced,
  state,
  getters,
  actions,
  mutations
};