import axios from 'axios';
import store from './store'; // Import the Vuex store
import router from './router';

const service = axios.create({
  baseURL: import.meta.env.VITE_Backend,
  withCredentials: true,
  xsrfCookieName: 'csrf_access_token', 
  headers: {
    'Content-Type': 'application/json',
    accept: 'multipart/form-data',
  },
});

// Request interceptor to add the token to headers
service.interceptors.request.use(
  (config) => {
    const token = store.getters['auth/StateToken'];
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    if (config.url === "/auth/logout") {
      store.commit('product/logoutUserState');
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token expiration and refresh
const COOKIE_EXPIRED_MSG = 'Token has expired'
service.interceptors.response.use((response) => {
  return response
}, async (error) => {
  const error_message = error.response.data.msg
  switch (error.response.status) {
    case 401:
      if (!error.config.retry && error_message === COOKIE_EXPIRED_MSG) {
        error.config.retry = true
          service.defaults.xsrfCookieName = 'csrf_refresh_token';
          service.defaults.xsrfCookieName = 'csrf_access_token';
          
          store.commit('auth/logoutUserState');
          store.commit('product/logoutUserState');
          router.push({ name: 'signin' });
          /*
          const refresh_token = store.getters['auth/StateRefreshToken'];
          const config = {
            // Use the refresh token from the Vuex store
            headers:{ 'Authorization': `Bearer ${refresh_token}`}
          };

          await service.post('/auth/refresh', {}, config)
          .then((response)=>{
            const newToken = response.data['access_token'];
  
            // Update the token in the Vuex store
            store.commit('auth/setToken', newToken, refresh_token);
    
            // Update the token in the headers and retry the original request
            service.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
            error.config.headers['Authorization'] = `Bearer ${newToken}`;
    
            return service(error.config);
          }, (refreshError)=>{
            // Handle token refresh failure 
            store.commit('auth/logoutUserState');
            store.commit('product/logoutUserState');
            router.push({ name: 'signin' });
            return Promise.reject(refreshError);
          });
        */
      }
      break;
    case 404:
      router.push({ name: 'not_found' });
      break;
    default:
      break;
  }
  return Promise.reject(error.response);
});

export { service };

