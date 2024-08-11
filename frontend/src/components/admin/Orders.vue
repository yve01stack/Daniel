<template>
<div v-if="orders.length === 0">
    <EmptyLayout message="Pas de commandes" />
</div>

<div v-else class="order_container">
    <div class="column">
        <div class="header_line_title">
            <h3>Commande Details</h3>
        </div>

        <div v-if="selectedOrder" class="order_processing">
            <OrderProcess 
            :selectedOrder="selectedOrder" 
            :orders="orders"
            :active="active" />
        </div> 
        <div v-else>
            <EmptyLayout message="Sélectionnez une commande pour voir les détails" />
        </div>
    </div>
    
    <div class="column">
        <div class="header_line_title">
            <h3>Commandes ({{ orders.length }})</h3>
        </div>
        <div class="order_content">

            <div class="order_item" :disabled="true"
            v-for="order in displayedOrders" 
            :key="order.id" 
            @click="selectOrder(order)">
                <i class="fad fa-shipping-fast icon"></i>
                <div class="order_item_desc">
                    <div style="margin-bottom: 5px;">
                        <small style="font-weight: 600;">
                            {{ order.order_number }} ({{ order.order_items.length }}), {{ order.created_on }} 
                        </small>
                        <el-tag v-if="order.canceled" style="float: right; width: 80px;" type="info" effect="light" round>Annulée</el-tag>
                        <el-tag v-else-if="order.delivered" style="float: right; width: 80px;" type="success" effect="light" round>Livrée</el-tag>
                        <el-tag v-else style="float: right; width: 80px;" type="primary" effect="light" round>En cours</el-tag>
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="font-weight: 700;">{{ order.total_price }} {{ order.currency }}</span>
                        <span v-if="order.paid_confirmed == 'submitted'" style="font-weight: 500; color: rgb(133, 212, 255);"> | envoyé</span>
                        <span v-else-if="order.paid_confirmed == 'rejected'" style="font-weight: 500; color: rgb(249, 129, 129);"> | refusé</span>
                        <span v-else-if="order.paid_confirmed == 'confirmed'" style="font-weight: 500; color: rgb(123, 242, 123);"> | approuvé</span>
                
                        <el-button v-if="order.paid_confirmed == 'confirmed'"
                            :disabled="order.delivered"
                            @click="cancelOrder(order.id)"
                            style="float: right; padding: 0 18px 0 18px;" 
                            size="small" 
                            type="warning" 
                            round plain>Annuler
                        </el-button> 
                        <el-button v-else
                            :disabled="order.delivered"
                            @click="removeOrder(order.id)"
                            style="float: right;" 
                            size="small" 
                            type="danger" 
                            round plain>Supprimer
                        </el-button>            
                    </div>
                </div>
            </div>

            <div class="page_buttons">
                <el-button size="small" @click="prevPage" :disabled="currentPage === 1">Précedent</el-button>
                <el-button size="small" @click="nextPage" :disabled="currentPage === totalPages">Suivant</el-button>
            </div>
        
        </div>
    </div>
</div>

</template>

<script setup>
import OrderProcess from './OrderProcess.vue'
import EmptyLayout from '../EmptyLayout.vue'
import { ElMessage } from 'element-plus';
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore()

const orders = computed(() => store.getters['admin/orders']);

const active = ref(1)

const selectedOrder = ref(null);

const fetchOrders = async () => {
    await store.dispatch('admin/fetchOrders');
};

const selectOrder = (order) => {
  selectedOrder.value = order;
  if (order.paid_confirmed == "confirmed") {
    active.value = 3;
  } else {
    active.value = 2;
  }
};

const removeOrder = async (id) => {
    await store.dispatch('admin/removeOrder', { orderId: id })
    .then((data) => {
        if (data.status === 'error'){
            ElMessage(data.message)
        }
    })
};

const cancelOrder = async (id) => {
    await store.dispatch('admin/cancelOrder', { orderId: id })
    .then((data) => {
        if (data.status === 'error'){
            ElMessage(data.message)
        }
    })
};


const currentPage = ref(1);
const pageSize = 5;

const totalPages = computed(() => Math.ceil(orders.value.length / pageSize));

const displayedOrders = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return orders.value.slice(start, end);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};


onMounted(() => {
    fetchOrders();
});  
</script>

<style scoped>
.order_container {
display: flex;
flex-wrap: wrap;
}

.order_container .column {
flex: 1;
box-sizing: border-box;
padding-right: 10px;
}

.header_line_title {
margin-top: 10px;
margin-bottom: 20px;
border-bottom: 3px solid #088178;
width: 70px;
white-space: nowrap;
overflow: visible;
}

/* Order items style */
.order_item {
border-top: 1px solid #eee; 
border-bottom: 1px solid #eee; 
width: 100%; 
display: flex; 
padding: 5px 10px;
cursor: pointer;
} 

.order_item:hover {
background-color: #eee;
}

.order_item:active {
background-color: #eee;
}

.order_item .icon {
font-size: 30px; 
margin-top: 14px;
object-fit: cover;
}

.order_item .order_item_desc {
flex-grow: 1; 
padding-left: 8px; 
align-content: center;
font-size: 14px;
}

.page_buttons {
  width: 100%;
  display: flex;
  justify-content: center;
  padding-top: 8px;
}


/* Media query for screens with a max-width of */

@media (max-width: 780px) {
.order_container .column {
    flex: 0 0 100%;
    padding-right: 0px;
}

}

</style>