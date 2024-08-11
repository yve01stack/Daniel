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
          :model="form"
          label-position="left" 
          label-width="auto" 
          style="max-width: 600px">              
        
        <el-space fill>
          <span style="font-size: 14px; color: #787878;">Adresse de livraison du client/ Informations de contact</span>  
          <el-input v-model="selectedOrderCopy.ordered_by.location" :disabled="true"
          placeholder="1007 Louis, Place Raponda Walker Libreville"/>
        </el-space>
        <el-space fill>
          <span style="height: 0px; overflow: hidden;">Adresse de livraison du client/ Informations de contact</span>  
          <el-row :gutter="20">
            <el-col :span="12">
              <el-input
                :disabled="true"
                v-model="selectedOrderCopy.ordered_by.email"
                aria-label="E-mail"
                placeholder="E-mail"
              />
            </el-col>
            <el-col :span="12">
              <el-input
                :disabled="true"
                v-model="selectedOrderCopy.ordered_by.phone"
                aria-label="Téléphone"
                placeholder="Téléphone"
              />
            </el-col>
          </el-row>
        </el-space>

        <el-space fill>
          <span style="color: burlywood; font-size: 14px;">
            Veuillez vérifier la conformité du payement via transfer mobile d'une somme de 
            <span style="color: cornflowerblue;">{{ selectedOrderCopy.total_price }} {{ selectedOrderCopy.currency }}</span> 
            à <span style="color: cornflowerblue;">{{ selectedOrderCopy.account_number }}</span>
            au nom de <span style="color: cornflowerblue;">{{ selectedOrderCopy.account_name }}</span>.
          </span>
          <span 
            v-if="selectedOrderCopy.paid_confirmed != 'none'"
            style="color: black; font-size: 14px;">Capture d'écran:
            <a :href="selectedOrderCopy.paid_proof" target="_blank" style="color: cornflowerblue;">télécharger</a>
          </span>
          <el-alert
            v-if="selectedOrderCopy.paid_confirmed == 'confirmed'" 
            :title="selectedOrderCopy.paid_desc" type="success" :closable="false" />
          <el-alert
            v-if="selectedOrderCopy.paid_confirmed == 'rejected'" 
            :title="selectedOrderCopy.paid_desc" type="error" :closable="false" />
          <span style="color: black; font-size: 14px;">Décision
            <el-input v-model="form.paid_desc" type="textarea" />
          </span>
          </el-space>
      </el-form>
    </div>

    <div v-if="activeCopy === 3">
      <MapComponent 
        :selectedOrder="selectedOrderCopy"/>

      <div v-if="!selectedOrderCopy.delivered">
        <el-form :model="deliveredForm">
            <el-input size="small" v-model="deliveredForm.delivery_number" placeholder="No. de livraison" style="margin-bottom: 3px;"/>
            <el-input  size="small" v-model="deliveredForm.delivery_center" placeholder="Point de livraison" style="margin-bottom: 3px;"/>
          <el-button size="small" @click="orderDelivery(selectedOrderCopy.id)">Marquer Livrée</el-button>
        </el-form>
      </div>
    </div>

    <el-button-group style="margin-top: 12px; float: right;">
      <el-button 
      style="padding: 0 5px 0 5px;"
      round type="primary" @click="prev" :icon="ArrowLeft" />
      <el-tooltip content="Approuver l'authenticité et la conformité du paiement" placement="top" effect="light">
        <el-button
        style="padding: 0 5px 0 5px;" 
        :disabled="selectedOrderCopy.paid_confirmed === 'confirmed' | activeCopy != 2" 
        round type="success"
        @click="confirmProof(selectedOrderCopy.id, 'confirmed')" :icon="DocumentChecked" />  
      </el-tooltip>
      <el-tooltip content="Rejeter l'authenticité et la conformité du paiement" placement="top" effect="light">
        <el-button
        style="padding: 0 5px 0 5px;" 
        :disabled="selectedOrderCopy.paid_confirmed == 'confirmed' | activeCopy != 2"
        round type="danger" 
        @click="confirmProof(selectedOrderCopy.id, 'rejected')" :icon="DocumentDelete" />
      </el-tooltip>
      <el-button 
      style="padding: 0 5px 0 5px;"
      round type="primary" @click="next" :icon="ArrowRight" />
    </el-button-group>

</template>

<script setup>
import MapComponent from '../MapComponent.vue'
import OrderedProduct from '../OrderedProduct.vue'
import { 
  Edit, 
  CreditCard, 
  LocationFilled, 
  ArrowLeft, 
  ArrowRight,
  DocumentChecked,
  DocumentDelete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus';
import { ref, defineProps, toRaw, watch } from 'vue';
import { useStore } from 'vuex';

const store = useStore()

const props = defineProps({
    active: { type: Number, required: true},
    selectedOrder: { type: Object, required: true },
    orders: { type: Object, required: true }
});

const ordersCopy = ref(props.orders);

watch(() => props.orders, (newValue) => {
  ordersCopy.value = newValue;
});

const selectedOrderCopy = ref(props.selectedOrder);

watch(() => props.selectedOrder, (newValue) => {
  selectedOrderCopy.value = newValue;
});

const activeCopy = ref(props.active);

watch(() => props.active, (newValue) => {
  activeCopy.value = newValue;
});

const next = () => {
  if (selectedOrderCopy.value.paid_confirmed == "confirmed") {
    if (activeCopy.value++ > 2) activeCopy.value = 3;
  } else {
    if (activeCopy.value++ > 1) activeCopy.value = 2;
  }
}

const prev = () => {
  if (activeCopy.value-- < 2) activeCopy.value = 1;
}

const form = ref({ paid_desc: '' });

const confirmProof = async (orderId, paid_confirmed) => {
  const formData = {
    orderId: orderId, 
    paid_desc: form.value.paid_desc,
    paid_confirmed: paid_confirmed
  }

  await store.dispatch('admin/confirmProof', formData)
  .then((data) => {
    selectedOrderCopy.value = ordersCopy.value.find(order => order.id === orderId);

    if (data.status === 'success'){
      ElMessage(data.message)
    } else {
      ElMessage.error(data.message)
    }
  })
};

const deliveredForm = ref({
  orderId: '',
  delivery_number: '',
  delivery_center: ''
})

const orderDelivery = async (orderId) => {

  deliveredForm.value.orderId = orderId;

  await store.dispatch('admin/orderDelivery', toRaw(deliveredForm.value))
  .then((data) => {
    selectedOrderCopy.value = ordersCopy.value.find(order => order.id === orderId);

    if (data.status === 'success'){
      ElMessage(data.message)
      deliveredForm.value.orderId = '';
      deliveredForm.value.delivery_number = '';
      deliveredForm.value.delivery_center = '';
    } else {
      ElMessage.error(data.message)
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