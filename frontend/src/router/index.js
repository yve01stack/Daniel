import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignIn from '../views/SignIn.vue'
import SignUp from '../views/SignUp.vue'
import NotFound from '../views/NotFound.vue'
import ProfileView from '../views/ProfileView.vue'
import ProductDetail from '../views/ProductDetail.vue'
import ProductView from '../views/ProductView.vue'
import CheckEmail from '../views/CheckEmail.vue'
import ResetPassword from '../views/ResetPassword.vue'
import AdminView from '../views/AdminView.vue'
import AboutView from '../views/AboutView.vue'
import AdminDashboard from '../components/admin/Dashboard.vue'
import AdminAddProduct from '../components/admin/AddProduct.vue'
import AdminOrders from '../components/admin/Orders.vue'
import AdminUpdateProduct from '../components/admin/UpdateProduct.vue'
import AdminUser from '../components/admin/User.vue'

import store from "../store";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView, meta: { guest: true } },
    { path: '/signin', name: 'signin', component: SignIn, meta: { guest: true } },
    { path: '/signup', name: 'signup', component: SignUp, meta: { guest: true } },
    { path: '/about', name: 'about', component: AboutView, meta: { guest: true } },
    { 
      path: '/product', 
      name: 'product', 
      meta: { guest: true },
      children: [
        { path: 'all', name: 'products', component: ProductView },
        { path: ':id', name: 'product_detail', component: ProductDetail },
      ]
    },
    { 
      path: '/user', 
      name: 'user',
      children: [
        { path: 'check_email/:token', name: 'check_email', component: CheckEmail, meta: { guest: true } },
        { path: 'reset_password/:token', name: 'reset_password', component: ResetPassword, meta: { guest: true } },
        { path: 'profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true }, },
      ]
    },
    { 
      path: '/admin', 
      name: 'admin', 
      component: AdminView, 
      meta: {requiresModerator: true}, 
      redirect: '/admin/dashboard',
      children: [
        { path: 'dashboard', name: 'admin_dashboard', components: { admin: AdminDashboard } },
        { path: 'user', name: 'admin_user', components: { admin: AdminUser }, meta: {requiresAdmin: true}, },
        { path: 'order', name: 'admin_order', components: { admin: AdminOrders }, },
        { path: 'product', 
          name: 'admin_product', 
          meta: {requiresAdmin: true},
          children: [
            { path: 'add', name: 'admin_product_add', components: { admin: AdminAddProduct }, },
            { path: 'update', name: 'admin_product_update', components: { admin: AdminUpdateProduct }, },

          ]
        },
        
      ]
    },

    { path: '/:pathMatch(.*)*', name: 'not_found', component: NotFound },

  ],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  },
});


router.beforeEach((to, from, next) => {
  const isLoggedIn = store.getters['auth/isLoggedIn'];
  const isAdmin = store.getters['auth/isAdmin']; 
  const isModerator = store.getters['auth/isModerator']; 

  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Check if the user is logged in
    if (isLoggedIn) {
      
      // If the route requires moderator privileges
      if (to.matched.some(record => record.meta.requiresModerator)) {
        if (isModerator) {
          
          if (to.matched.some(record => record.meta.requiresAdmin)) {
            if (isAdmin) {
              next(); // User is an admin, proceed to route
            } else {
              next('/unauthorized'); // Redirect to an unauthorized page or a different route
            }
          } else {
            next(); // No admin privileges required, proceed to route
          }

        } else {
          next('/unauthorized'); // Redirect to an unauthorized page or a different route
        }

      } else {
        next(); // No moderator privileges required, proceed to route
      }

    } else {
      next('/signin'); // Redirect to sign-in page if not logged in
    }

  } else if (to.matched.some(record => record.meta.guest)) {
    // If the route is for guests and the user is logged in, redirect to the home page
    if (isLoggedIn) {
      next();
    } else {
      next(); // User is not logged in, proceed to route
    }
  } else {
    next(); // No special auth requirements, proceed to route
  }
});


export default router
