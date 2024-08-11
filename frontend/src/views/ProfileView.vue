<template>
  <el-page-header title="Accueil" @back="onBack" style="width: 100%;">
    <template #content>
      <div style="display: flex; align-items: center;">
        
        <el-tooltip :content="userData.name" placement="top" effect="light">  
          <el-avatar style="margin-right: 5px;"
            :size="32"
            :src="userData.avatar"
          />
        </el-tooltip>
        <span class="user_name"> {{ userData.name }} </span>
      </div>
    </template>
    <template #extra>
      <div style="display: flex; align-items: center;">
        <el-button-group class="ml-4">
          <el-button size="small" @click="edictUser = true">Modifier</el-button>
          <el-tooltip
            v-if="userData.status === 'admin' || userData.status == 'moderator'" 
            content="Admin tableau de bord " 
            placement="top" effect="light">
             
              <el-button size="small" type="primary">
                <RouterLink to="/admin"><el-icon><Menu /></el-icon></RouterLink>
              </el-button>
            </el-tooltip>
        </el-button-group>
      </div>
    </template>

    <el-descriptions :column="2" size="small" class="mt-4">
      <!-- <el-descriptions-item label="Téléphone">{{ userData.phone }}</el-descriptions-item>
      <el-descriptions-item label="E-mail">{{ userData.email }}</el-descriptions-item>
      <el-descriptions-item label="Statut">
        <el-tag size="small">{{ userData.status }}</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="Adresse">{{ userData.location }}</el-descriptions-item> -->
    </el-descriptions>
    
    <div>
      <UserProfile :userData="userData" :orders="orders" />
    </div>

  </el-page-header>

  <!-- Edict User modal -->
  <el-dialog v-model="edictUser" width="340">
    <template #header="{titleId, titleClass }">
      <div>
        <h3 :id="titleId" :class="titleClass">Modifier votre compte</h3>
      </div>
    </template>
    <el-form
      label-position="top"
      ref="ruleFormRef"
      style="max-width: 400px"
      :model="ruleForm"
      status-icon
      :rules="rules"
      label-width="auto"
      class="demo-ruleForm"
    >
      <el-form-item label="Téléphone" prop="phone">
        <el-input 
          v-model="ruleForm.phone" 
          type="tel" 
          placeholder="Entrer un numéro de téléphone"/>
      </el-form-item>
      <el-form-item prop="email" label="E-mail">
        <el-input v-model="ruleForm.email" type="email"/>
        <el-button-group style="margin-top: 14px; float: right;">
          <el-button size="medium" plain round :icon="Edit" @click="edictEmail()"></el-button>
          <el-button size="medium" round type="primary" :disabled="userData.confirmed" @click="checkEmail()">Vérifier</el-button>
        </el-button-group>
      </el-form-item>
  
      <el-form-item label="Mot de Passe" prop="password">
        <el-input 
          v-model="ruleForm.password" 
          type="password" 
          autocomplete="off" 
          placeholder="Entrer un nouveau mot de passe"/>
      </el-form-item>
      <el-form-item prop="checkPass">
        <el-input
          v-model="ruleForm.checkPass"
          type="password"
          autocomplete="off"
          placeholder="Confirmer"
        />
      </el-form-item>
      <el-form-item>
        <el-button round @click="changePwd(ruleFormRef)" :icon="Edit">Changer</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>

</template>

<script lang="ts" setup>
import UserProfile from '../components/UserProfile.vue';
import { reactive, ref } from 'vue'

import type { FormInstance, FormRules } from 'element-plus'
import { Menu, Edit } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus';
import { useStore } from 'vuex';
import { computed, onMounted } from 'vue';
import router from '@/router';

const store = useStore()

const userData = computed(() => store.getters['auth/user']);
const orders = computed(() => store.getters['product/orders']);

const onBack = () => {
  router.push({ name: "home" })
}

// fetch orders and 
const fetchUser = async () => {
  await store.dispatch('auth/fetchUser');
};

const fetchOrders = async () => {
  await store.dispatch('product/fetchOrders');
};

const edictUser = ref(false);

const ruleFormRef = ref<FormInstance>()

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Veuillez saisir le mot de passe'))
  } else {
    if (ruleForm.checkPass !== '') {
      if (!ruleFormRef.value) return
      ruleFormRef.value.validateField('checkPass')
    }
    callback()
  }
}
const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Veuillez saisir à nouveau le mot de passe'))
  } else if (value !== ruleForm.password) {
    callback(new Error("Deux entrées ne correspondent pas !"))
  } else {
    callback()
  }
};

const ruleForm = reactive({
  phone: userData.value.phone,
  email: userData.value.email,
  password: '',
  checkPass: '',
});

const rules = reactive<FormRules<typeof ruleForm>>({
  password: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
  phone: [
        {
          required: true,
          message: 'Veuillez saisir un numéro de téléphone',
          trigger: 'blur',
        },
      ],
  email: [
        {
          required: true,
          message: 'Veuillez saisir une adresse e-mail',
          trigger: 'blur',
        },
        {
          type: 'email',
          message: 'Veuillez saisir une adresse e-mail correcte',
          trigger: ['blur', 'change'],
        },
      ],
});

const edictEmail = async () => {
  await store.dispatch('auth/edictEmail', ruleForm )
  .then((data) => {
    if (data.status === 'success') {
      ElMessage({message: data.message, type: 'success'})
    } else {
      ElMessage({message: data.message, type: 'error'})
    }
  })      
};

const checkEmail = async () => {
  await store.dispatch('auth/checkEmail', { baseUrl: 'http://localhost:5173/user/check_email/' })
  .then((data) => {
    if (data.status === 'success') {
      ElMessage({message: data.message, type: 'success'})
    } else {
      ElMessage({message: data.message, type: 'error'})
    }
  })      
};

const updatePwd = async (form: any) => {
  await store.dispatch('auth/changePwd', form)
  .then((data) => {
    if (data.status === 'success') {
      ElMessage({message: data.message, type: 'success'})
      ruleForm.password = '';
      ruleForm.checkPass = '';
    } else {
      ElMessage({message: data.message, type: 'error'})
    }
  })      
};

const changePwd = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      updatePwd(ruleForm)
    } else {
      console.log('error submit!')
    }
  })
};

onMounted(() => {
  fetchUser();
  fetchOrders();
});
</script>

<style scoped>
.user_name {
  font-size: 14px; 
  font-weight: 600;
}


@media (max-width: 477px) {

  .user_name {
    display: none;
  }
}
</style>