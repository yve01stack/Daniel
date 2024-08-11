<template>
    <div class="product_container customScrollbar">
        <div class="product_item" v-for="order_item in selectedOrderCopy.order_items">
            <div class="product_item-image">
              <router-link :to="{ name: 'product_detail', params: { id: order_item.product.id } }">  
                <img :src="order_item.product.imgSrc" :alt="order_item.product.title">
              </router-link>
            </div>
            <div class="product_item-details">
                <div class="product_item-title">{{ order_item.product.title }}</div>
                <div class="product_item-btn">
                    <button class="quantity-btn" @click="decreaseOrderItemQuantity(order_item.id, order_item.order_id)">-</button>
                    <input type="number" id="quantity-input" :value="order_item.quantity" min="1" readonly>
                    <button class="quantity-btn" @click="increaseOrderItemQuantity(order_item.id, order_item.order_id)">+</button>
                    <button class="delete-btn" @click="removeFromOrder(order_item.id, order_item.order_id)">Supprimer</button>
                </div>
                <div class="total-price">  
                    {{ order_item.product.price*order_item.quantity }} {{ order_item.product.currency }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, watch } from 'vue';
import { useStore } from 'vuex';

const props = defineProps({
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

const removeFromOrder = async (id, order_id) => {
  await store.dispatch('product/removeFromOrder', { orderItemId: id })
  .then((data) => {
    selectedOrderCopy.value = ordersCopy.value.find(order => order.order_id === order_id);
    if (data.status === 'error'){
      ElMessage(data.message)
    }
  })
};

const increaseOrderItemQuantity = async (id, order_id) => {
  await store.dispatch('product/increaseOrderItemQuantity', { orderItemId: id })
  .then((data) => {
    selectedOrderCopy.value = ordersCopy.value.find(order => order.order_id === order_id);
    if (data.status === 'error'){
      ElMessage(data.message)
    }
  })
};

const decreaseOrderItemQuantity = async (id, order_id) => {
  await store.dispatch('product/decreaseOrderItemQuantity', { orderItemId: id })
  .then((data) => {
    selectedOrderCopy.value = ordersCopy.value.find(order => order.order_id === order_id);
    if (data.status === 'error'){
      ElMessage(data.message)
    }
  })
};

</script>

<style scoped>
/* Product item style */
.product_container {
  padding-top: 5px;
  overflow-x: hidden;
}

.product_item {
    display: flex;
    align-items: center;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 6px;
    margin-bottom: 5px;
    background-color: #f9f9f9;
    height: 88px;
}

.product_item-image img {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
    margin-top: 6px;
}

.product_item-details {
    flex-grow: 1;
    padding-left: 10px;
}

.product_item-title {
    /* width: 90%; */
    width: 200px;
    font-size: 14px;
    justify-content: space-between;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.product_item-btn {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-top: 5px;
}

.product_item-btn .quantity-btn {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.product_item-btn .quantity-btn:hover {
    background-color: #2980b9;
}

.product_item-btn .delete-btn {
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.product_item-btn .delete-btn:hover {
    background-color: #c0392b;
}
#quantity-input {
    width: 30px;
    text-align: center;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px;
}

/* Chrome, Safari, Edge, Opera */
#quantity-input::-webkit-outer-spin-button,
#quantity-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
#quantity-input {
  -moz-appearance: textfield;
}

.total-price {
    margin-top: 5px;
    font-size: 14px;
    font-weight: bold;
    color: #333;
}

</style>