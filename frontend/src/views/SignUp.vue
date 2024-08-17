<template>
  <div class="form_container">
    <div class="register_form">
      <div>
        <h3 style="text-align: center; margin-bottom: 20px;">Inscrivez-vous</h3>
        <el-alert v-if="registerResponse.status" :title="registerResponse.msg" :type="registerResponse.type" 
            :closable="false" show-icon style="background-color: transparent;" />
        <el-form
          ref="ruleFormRef"
          style="max-width: 400px"
          :model="ruleForm"
          :rules="rules"
          label-width="auto"
          class="demo-ruleForm"
          :size="formSize"
          label-position="top"
          status-icon
        >
          <el-form-item label="Nom/Prénoms" prop="name">
            <el-input v-model="ruleForm.name" />
          </el-form-item>
          <el-form-item label="E-mail" prop="email">
            <el-input v-model="ruleForm.email" placeholder="exemple@gmail.com"/>
          </el-form-item>
          <el-form-item label="Téléphone" prop="phone">
            <el-input v-model="ruleForm.phone" placeholder="12345678"/>
          </el-form-item>
          <el-form-item label="Mot de passe" prop="password">
            <el-input v-model="ruleForm.password" type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item label="Confirme" prop="checkPass">
            <el-input v-model="ruleForm.checkPass" type="password" autocomplete="off" />
          </el-form-item>    
          <el-form-item label="Domicile" prop="location">
            <el-input v-model="ruleForm.location" placeholder="1007 Louis, Place Raponda Walker Libreville"/>
          </el-form-item>
          <el-form-item>Si vous avez déjà un compte
            <RouterLink to="/signin">
              <span style="color:cornflowerblue">, connectez-vous!</span>
            </RouterLink>
          </el-form-item>
          <el-form-item>
            <div  style="display: flex; justify-content: center; width: 100%;">
              <el-button type="primary" @click="submitForm(ruleFormRef)">
                S'inscrire
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>

</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'; 

const router = useRouter();
const store = useStore()

interface RuleForm {
  name: string
  email: string
  phone: string
  password: string
  checkPass: string
  location: string
}

const formSize = ref<ComponentSize>('default')
const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive<RuleForm>({
  name: '',
  email: '',
  phone: '',
  password: '',
  location: '',
  checkPass: '',
})

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
};

const validatePass2 = (rule: any, value: any, callback: any) => {
    if (value === '') {
      callback(new Error('Veuillez saisir encore le mot de passe'))
    } else if (value !== ruleForm.password) {
      callback(new Error("les deux mots de passe ne correspondent pas"))
    } else {
      callback()
    }
};

const rules = reactive<FormRules<RuleForm>>({
  name: [
    { required: true, message: 'Veuillez saisir le nom/prénoms', trigger: 'blur' },
    { min: 5, max: 30, message: 'La nom/prénoms doit être de 5 à 30 caractètes', trigger: 'blur' },
  ],
  email: [
    {
      required: false,
      message: 'Veuillez saisir l\'adresse e-mail',
      trigger: 'blur',
    },
    {
      type: 'email',
      message: 'Veuillez saisir une adresse e-mail correcte',
      trigger: ['blur', 'change'],
    },
  ],
  phone: [
    {
      required: true,
      message: 'Veuillez saisir le numéro de téléphone',
      trigger: 'blur',
    },
  ],
  password: [
    { 
      required: true,
      message: 'Veuillez saisir le mot de passe',
      validator: validatePass, 
      trigger: 'blur'
    },
    { min: 5, max: 30, message: 'La mot de passe doit être de 5 à 30 caractètes, symboles et chiffres', trigger: 'blur' },

  ],
  checkPass: [
    { 
      validator: validatePass2, 
      trigger: 'blur' 
    }
  ],
  location: [
    {
      required: false,
      message: 'Veuillez donner une adresse',
      trigger: 'change',
    },
  ],

})

const registerResponse = reactive({status: false, type: 'success', msg: ""});

const register = async () => {
  await store.dispatch('auth/registerUser', ruleForm)
  .then((data) => {
    if (data.status==="success") {
      registerResponse.status = true;
      registerResponse.type = 'success';
      registerResponse.msg = data.message;
      router.push({ name: 'home' })
    } else {
      registerResponse.status = true;
      registerResponse.type = 'error';
      registerResponse.msg = data.message;
    }
  }) 
};

const submitForm =  (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      register()
    } else {
      console.log('error submit!')
    }
  })
};

</script>

<style scoped>

.form_container {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  .register_form {
    max-width: 400px;
    display: flex;
    justify-content: center;
    border-radius: 5px;
    box-shadow: 1px 1px 10px 10px rgba(186,191,203,0.08);
    padding: 20px;
  }
</style>