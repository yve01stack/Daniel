<template>
    <el-steps class="order_step_sm"
        :space="200"
        :active="activeCopy"
        finish-status="success"
        simple
    >
        <el-step :icon="Edit" />
        <el-step :icon="CreditCard" />
        <el-step :icon="LocationFilled" />
    </el-steps>

    <el-steps class="order_step_lg"
        :space="200"
        :active="activeCopy"
        finish-status="success"
        simple
    >
        <el-step title="Produits" :icon="Edit" />
        <el-step title="Livraison" :icon="CreditCard" />
        <el-step title="Complète" :icon="LocationFilled" />
    </el-steps>

    <div v-if="activeCopy === 1">
      <OrderedProduct 
      :selectedOrder="selectedOrderCopy" 
      :orders="ordersCopy" />
        <h3>Montant total: {{ selectedOrderCopy.total_price }} {{ selectedOrderCopy.currency }}</h3>
    </div>

    <div v-if="activeCopy === 2">
        <el-form 
        label-position="left" 
        label-width="auto" 
        style="max-width: 600px"
        v-model="formDelivery">              
        
        <el-space fill>
            <span style="height: 0px; overflow: hidden; ">
            Si vous modifiez votre numéro de téléphone et/ou votre email, 
                il devient votre identifiant de connexion et/ou votre adresse principale.
            </span>  
            <el-alert 
            v-if="submitProofResponse.status" 
            :title="submitProofResponse.msg" 
            :type="submitProofResponse.type" 
            :closable="false" :show-icon="true" 
            style="background-color: transparent; margin: 0 -16px 0 -16px;" />
            <el-input v-model="formDelivery.location"
            placeholder="1007 Louis, Place Raponda Walker Libreville"/>
        </el-space>
        <el-space fill>
            <span style="font-size: 14px; color: #787878;">
                Informations de contact
            </span>
            <el-row :gutter="20">
                <el-col :span="12">
                <el-input
                    :disabled="true"
                    v-model="formDelivery.email"
                    aria-label="E-mail"
                    placeholder="E-mail"
                />
                </el-col>
                <el-col :span="12">
                <el-input
                    :disabled="true"
                    v-model="formDelivery.phone"
                    aria-label="Téléphone"
                    placeholder="Téléphone"
                />
                </el-col>
            </el-row>
        </el-space>

        <el-space fill>
        <span style="color: burlywood; font-size: 14px;">
            Veuillez télécharger une capture d'écran de votre transfer mobile d'une somme de 
            <span style="color: cornflowerblue;">{{ selectedOrderCopy.total_price }} {{ selectedOrderCopy.currency }}</span> 
            à <span style="color: cornflowerblue;">{{ selectedOrderCopy.account_number }}</span>
            au nom de <span style="color: cornflowerblue;">{{ selectedOrderCopy.account_name }}</span>.
        </span>
        <span 
            v-if="selectedOrderCopy.paid_confirmed != 'none'"
            style="color: black; font-size: 14px;">Capture d'écran:
            <a :href="selectedOrderCopy.paid_proof" target="_blank" style="color: cornflowerblue;">télécharger</a>
        </span>
        <span style="color: black; font-size: 14px;">
            Agent: {{ selectedOrderCopy.managed_by.name }}, 
            <a :href="'tel:'+selectedOrderCopy.managed_by.phone">
                {{ selectedOrderCopy.managed_by.phone }}
            </a>, 
            <a :href="'mailto:'+selectedOrderCopy.managed_by.email">
                {{ selectedOrderCopy.managed_by.email }}
            </a>
        </span>
        <el-alert
            v-if="selectedOrderCopy.paid_confirmed == 'confirmed'" 
            :title="selectedOrderCopy.paid_desc" type="success" :closable="false" />
        <el-alert
            v-if="selectedOrderCopy.paid_confirmed == 'rejected'" 
            :title="selectedOrderCopy.paid_desc" type="error" :closable="false" />
        <el-upload style="width: 100%;"
            class="upload-demo"
            drag
            :auto-upload="false"
            :limit="1"
            :on-change="handleFile"
            :on-remove="handleFile"
            :on-exceed="handleFile"
            :file-list="fileList"
        >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">                  
            Déposez le fichier ici ou <em>cliquez pour télécharger</em>
            </div>
            <template #tip>
            <div class="el-upload__tip">
                Fichiers jpg/png d'une taille inférieure à 500 Ko
            </div>
            </template>
        </el-upload>
        </el-space>
      </el-form>
    </div>

    <div v-if="activeCopy === 3">
        <MapComponent 
        :selectedOrder="selectedOrderCopy"/>
    </div>

    <el-button-group style="margin-top: 12px; float: right;">
        <el-button 
        style="padding: 0 5px 0 5px;"
        round type="primary" @click="prev" :icon="ArrowLeft" />
        <el-button style="padding: 0 5px 0 5px;"
        :disabled="selectedOrderCopy.paid_confirmed == 'confirmed' | activeCopy != 2" 
        round type="primary"
        @click="submitProof(selectedOrderCopy.id)">Envoyer</el-button>
        <el-button 
        style="padding: 0 5px 0 5px;"
        round type="primary" @click="next" :icon="ArrowRight" />
    </el-button-group>

</template>

<script setup>
import MapComponent from '../MapComponent.vue'
import OrderedProduct from '../OrderedProduct.vue'
import { ref, reactive, defineProps, watch } from 'vue';
import { useStore } from 'vuex';
import { 
  Edit, 
  CreditCard, 
  LocationFilled, 
  UploadFilled, 
  ArrowLeft, 
  ArrowRight } from '@element-plus/icons-vue'

const props = defineProps({
    active: { type: Number, required: true},
    selectedOrder: { type: Object, required: true },
    orders: { type: Object, required: true }
});

const store = useStore()

const selectedOrderCopy = ref(props.selectedOrder);
  
watch(() => props.selectedOrder, (newValue) => {
    selectedOrderCopy.value = newValue;
});

const ordersCopy = ref(props.orders);

watch(() => props.orders, (newValue) => {
  ordersCopy.value = newValue;
});

const activeCopy = ref(props.active);

watch(() => props.active, (newValue) => {
  activeCopy.value = newValue;
});

const next = () => {
  if (selectedOrderCopy.value.paid_confirmed === 'confirmed') {
    if (activeCopy.value++ > 2) activeCopy.value = 3;
  } else {
    if (activeCopy.value++ > 1) activeCopy.value = 2;
  }
}

const prev = () => {
  if (activeCopy.value-- < 2) activeCopy.value = 1;
}

const fileList = ref([]);
const handleFile = (file, fileList) => {
  formDelivery.value.file = fileList.length > 0 ? fileList[0].raw : null;
  fileList.value = fileList;
};

const formDelivery = ref({
  location: selectedOrderCopy.value.ordered_by.location,
  email: selectedOrderCopy.value.ordered_by.email,
  phone: selectedOrderCopy.value.ordered_by.phone,
  file: null
});

const submitProofResponse = reactive({status: false, type: 'success', msg: ""});

const submitProof = async (orderId) => {

  if (!formDelivery.value.file) {
    submitProofResponse.status = true;
    submitProofResponse.type = 'error';
    submitProofResponse.msg = "Veuillez d'abord sélectionner un fichier (capture d'écran du paiement)";
    return ;
  } else if (formDelivery.value.location === '') {
    submitProofResponse.status = true;
    submitProofResponse.type = 'error';
    submitProofResponse.msg = "Veuillez saisir votre adresse";
    return ;
  } else {
    submitProofResponse.status = false;
  }

  var formData = new FormData();
  formData.append("orderId", orderId);
  formData.append("location", formDelivery.value.location);
  formData.append("file", formDelivery.value.file);

  await store.dispatch('product/paidProofOrder', formData)
  .then((data) => {
    selectedOrderCopy.value = ordersCopy.value.find(order => order.id === orderId);

    if (data.status === 'success'){
      submitProofResponse.status = true;
      submitProofResponse.type = 'success';
      submitProofResponse.msg = data.message;
    } else {
      submitProofResponse.status = true;
      submitProofResponse.type = 'error';
      submitProofResponse.msg = data.message;
    }
  })
};

</script>

<style scoped>

/* Order step style */
.order_step_sm {
  max-width: 600px; 
  margin-bottom: 10px;
  display: none;
}

.order_step_lg {
  max-width: 600px; 
  margin-bottom: 10px;
}

/* Media query for screens with a max-width of */

@media (max-width: 1390px) {
  .order_step_sm {
    display: flex;
  }

  .order_step_lg {
    display: none;
  }
}

@media (max-width: 780px) {

  .order_step_sm {
    display: none;
  }

  .order_step_lg {
    display: flex;
  }
}

@media (max-width: 600px) {

  .order_step_sm {
    display: flex;
  }

  .order_step_lg {
    display: none;
  }
}

</style>