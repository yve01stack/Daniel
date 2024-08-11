<template>
  <div class="container">
    <div class="login_form">
      <div>
        <h3 style="text-align: center; margin-bottom: 20px;">Connectez-vous</h3>
        <el-alert v-if="loginResponse.status" :title="loginResponse.msg" :type="loginResponse.type" 
          :closable="false" show-icon style="background-color: transparent;" />
        <el-form
          ref="ruleFormRef"
          style="max-width: 460px"
          :model="ruleForm"
          status-icon
          :rules="rules"
          label-width="auto"
          class="demo-ruleForm"
        >
        <el-form-item label="Téléphone" prop="phone">
          <el-input v-model="ruleForm.phone" type="tel"/>
        </el-form-item>
        <el-form-item label="Mot de Passe" prop="password">
            <el-input v-model="ruleForm.password" type="password" />
        </el-form-item> 
        <el-form-item>Si vous n'avez pas un compte
            <RouterLink to="/signup">
                <span style="color:cornflowerblue">, inscrivez-vous!</span>
            </RouterLink>
        </el-form-item>
        <el-form-item style="margin-top: -20px;">
          <span @click="forgetPwd = true" style="color:cornflowerblue; cursor: pointer;">Mot de passe oublié ?</span>
        </el-form-item>
        <el-form-item>
          <div  style="display: flex; justify-content: center; width: 100%;">
            <el-button type="primary" @click="submitForm(ruleFormRef)">
              Se connecter
            </el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</div>

  <!-- password recovery modal -->
  <el-dialog v-model="forgetPwd" width="340">
    <template #header="{titleId, titleClass }">
      <div>
        <h3 :id="titleId" :class="titleClass">Récuperation de mot de passe</h3>
      </div>
    </template>
    <el-form :model="pwdForm">
      <el-form-item>
        <el-alert v-if="resetResponse.status" :title="resetResponse.msg" :type="resetResponse.type" 
          :closable="false" show-icon style="background-color: transparent;" />
      </el-form-item>
      <el-form-item label="E-mail">
        <el-input v-model="pwdForm.email" autocomplete="off" :required="true" type="email"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="forgetPwd = false">Retour</el-button>
        <el-button type="primary" @click="forgotPassword">
          Réinitialiser
        </el-button>
      </div>
    </template>
  </el-dialog>

</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'; 

const router = useRouter();
const store = useStore()

const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive({
    phone: '',
    password: '',
})

const rules = reactive<FormRules<typeof ruleForm>>({
    phone: [{ required: true, message: 'Veuillez saisir le numéro de téléphone', trigger: 'blur' }],
    password: [{ required: true, message: 'Veuillez saisir le mot de passe', trigger: 'blur' }],
})

const loginResponse = reactive({status: false, type: 'success', msg: ""});

const login = async () => {
  await store.dispatch('auth/loginUser', ruleForm)
  .then((data) => {
    if (data.status==="success") {
      loginResponse.status = true;
      loginResponse.type = 'success';
      loginResponse.msg = data.message;
      router.push({ name: 'home' })
    } else {
      loginResponse.status = true;
      loginResponse.type = 'error';
      loginResponse.msg = data.message;
    }
  }) 
};

// forget pwd 
const forgetPwd = ref(false)

const pwdForm = reactive({
  email: '',
  baseUrl: 'http://localhost:5173/user/reset_password/',
});

const resetResponse = reactive({status: false, type: 'success', msg: ""});

const forgotPassword = async () => {
  if (pwdForm.email === "") {
    resetResponse.status = true;
    resetResponse.type = 'error';
    resetResponse.msg = "Veuillez saisir l'adresse mail de votre compte";
    return 
    }
  await store.dispatch('auth/forgotPassword', pwdForm)
  .then((data) => {
    if (data.status==="success") {
      resetResponse.status = true;
      resetResponse.type = 'success';
      resetResponse.msg = data.message;
    } else {
      resetResponse.status = true;
      resetResponse.type = 'error';
      resetResponse.msg = data.message;
    }
  }) 
};

const submitForm =  (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      login()
    } else {
      console.log('error submit!')
    }
  })
};

</script>

<style scoped>

  .container {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  .login_form {
    max-width: 400px;
    display: flex;
    justify-content: center;
    border-radius: 5px;
    box-shadow: 1px 1px 10px 10px rgba(186,191,203,0.08);
    padding: 20px;
  }

</style>