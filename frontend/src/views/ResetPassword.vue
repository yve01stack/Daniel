<template>
    <el-result v-if="confirmed"
        icon="success"
        title="Confirmé"
        :sub-title="desc"
        >
        <template #extra>  
            <RouterLink to="/user/profile">
                <el-button round>Profil</el-button>
            </RouterLink>
        </template>
    </el-result>
    
    <el-result v-else
        icon="error"
        title="Erreur"
        :sub-title="desc"
        >
        <template #extra>
            <RouterLink to="/signin">
                <el-button round>Ré-essayer</el-button>
            </RouterLink>        
        </template>
    </el-result>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex'; 

const route = useRoute();
const store = useStore()

const confirmed = ref(false);
const desc = ref('');

const resetPassword = async () => {
    await store.dispatch('auth/resetPassword', {token: route.params.token})
    .then((data) => {
        desc.value = data.message;
        if (data.status === 'success') {
            confirmed.value = true;
        } else {
            confirmed.value = false;
        }
    })      
};

onMounted(() => {
    resetPassword();
});
</script>