<template>
    <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
      <el-radio-button size="small" :value="false">expand</el-radio-button>
      <el-radio-button size="small" :value="true">collapse</el-radio-button>
    </el-radio-group>
    
    <div style="display: flex;">
      <el-menu
        default-active="2"
        class="el-menu-vertical-demo"
        :collapse="isCollapse"
        :router="true"
        popper-effect="light"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-menu-item index="/admin/dashboard">
          <el-icon><PieChart /></el-icon>
          <template #title>Tableau de Bord</template>
        </el-menu-item>
        <el-sub-menu index="1">
          <template #title>
            <el-icon><FolderOpened /></el-icon>
            <span>Produits</span>
          </template>
          <el-menu-item-group>
            <template #title><span>Produits</span></template>
            <el-menu-item index="/admin/product/add">Ajouter</el-menu-item>
            <el-menu-item index="/admin/product/update">Mise à Jour</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="Group Two">
            <el-menu-item index="1-3">item three</el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>
        <el-menu-item index="/admin/order">
          <el-icon><Ticket /></el-icon>
          <template #title>Commandes</template>
        </el-menu-item>
        <el-menu-item index="/admin/user">
          <el-icon><UserFilled /></el-icon>
          <template #title>Utilisateur</template>
        </el-menu-item>
      </el-menu>

      <!-- Router view to display the current route's component -->
      <div style="margin-left: 8px; width: 100%;">
        <router-view name="admin"></router-view>
      </div>
    </div>

  </template>
  
  <script setup>
  import { ref } from 'vue'
  import {
    PieChart,
    UserFilled,
    FolderOpened, 
    Ticket
  } from '@element-plus/icons-vue'
  import { useRouter } from 'vue-router';

  // Use router instance
  const router = useRouter();

  
  const isCollapse = ref(true)
  const handleOpen = (key, keyPath) => {
    console.log(key, keyPath)
  }
  const handleClose = (key, keyPath) => {
    console.log(key, keyPath)
  }
  </script>
  
  <style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
  </style>
  