<template>
  <div class="dashboard_container">
      <div v-for="item in dashboard.statistic" class="wrimagecard wrimagecard-topimage">
          <div class="wrimagecard-topimage_header">
              <i :class="item.icon"></i>
              <div class="wrimagecard_value">
                  <sapn v-if="item.ratio === ''" style="color: rgb(0, 162, 255); font-weight:700">{{ item.value }}</sapn> 
                  <span v-else>
                      <el-tooltip
                      placement="top"
                      effect="light"
                      :content="item.labels.value"
                      >
                          <sapn style="color: rgb(0, 162, 255); font-weight:700">{{ item.value }}</sapn> 
                      </el-tooltip>\
                      <el-tooltip
                      placement="top"
                      effect="light"
                      :content="item.labels.ratio"
                      >
                          <span style="color: gray;">{{ item.ratio }}</span>
                      </el-tooltip>
                  </span>
              </div>
          </div>
          <div class="wrimagecard-topimage_title">
              <sapn style="font-weight:700">{{ item.name }}</sapn>
          </div>
      </div>
    </div>

  <!-- Chart -->
  <div class="form_session">
    <el-form :inline="true" :model="chartForms" @submit.prevent="updateChartData">
      <el-form-item>
        <el-select 
        v-model="chartForms.year" 
        placeholder="Année" 
        style="width: 100px;"
        >
          <el-option value="">Tout</el-option>
          <el-option v-for="year in availableYears" :key="year" :value="year" :label="year" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select 
        v-model="chartForms.month" 
        placeholder="Mois" 
        style="width: 100px;"
        >
          <el-option value="">Tout</el-option>
          <el-option v-for="month in availableMonths" 
          v-if="chartForms.year !==''"
          :key="month" 
          :value="month" 
          :label="month" />
        </el-select>
      </el-form-item>
    </el-form>
  </div>

  <div class="chart_session">
    <div class="chart_item">
      <OrderChart 
      :date="chartData.date" 
      :orders="chartData.orders" 
      :delivered_orders="chartData.delivered_orders"  />
    </div>
    <div class="chart_item">
      <ProductChart :data="productChart"/> 
    </div>
  </div>

</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import OrderChart from './OrderChart.vue';
import ProductChart from './ProductChart.vue';

const store = useStore()

const dashboard = computed(() => store.getters['admin/dashboard']);

// Process data to populate productChart
const productChart = computed(() => {
  
  const chart_data = ref({categories: [], products: [], carts: []});

  dashboard.value.top_products.forEach(product => {
    chart_data.value.categories.push(product.title);
    chart_data.value.products.push(product.quantities);
    
    const cart = dashboard.value.related_carts.find(cart => cart.id === product.id);
    chart_data.value.carts.push(cart ? cart.quantities : 0);
  });
  return chart_data;
});

// Process data to populate orderChart
const chartForms = ref({ year: '', month: '' });
const chartData = ref({ date: [], orders: [], delivered_orders: []});

// Function to update chart data
const updateChartData = () => {
  const selectedYear = chartForms.value.year;
  const selectedMonth = selectedYear !== "" ? chartForms.value.month : "";
  chartForms.value.month = selectedMonth; //update the form

  const processData = (data) => {
    return data.reduce((acc, order) => {
      const orderDate = new Date(order.date);
      const year = orderDate.getFullYear();
      const month = orderDate.getMonth() + 1;
      const day = orderDate.getDate();

      if (selectedYear && year !== parseInt(selectedYear)) return acc;
      if (selectedMonth && month !== parseInt(selectedMonth)) return acc;

      const key = selectedMonth ? `${year}-${month}-${day}` : selectedYear ? `${year}-${month}` : `${year}`;

      if (!acc[key]) acc[key] = 0;
      acc[key] += order.price;

      return acc;
    }, {});
  };

  const ordersData = processData(dashboard.value.orders);
  const deliveredOrdersData = processData(dashboard.value.delivered_orders);

  chartData.value.date = Object.keys(ordersData);
  chartData.value.orders = Object.values(ordersData);
  chartData.value.delivered_orders = Object.values(deliveredOrdersData);
};

watch(chartForms, updateChartData, { deep: true });

const availableYears = computed(() => {
  const years = new Set();
  dashboard.value.orders.forEach(order => {
    years.add(new Date(order.date).getFullYear());
  });
  return Array.from(years);
});

const availableMonths = computed(() => {
  return Array.from({ length: 12 }, (_, i) => i + 1);
});

updateChartData();



const fetchDashboard = async () => {
    await store.dispatch('admin/fetchDashboard');
};

onMounted(() => {
    fetchDashboard();
});  

</script>

<style scoped>
.el-form--inline .el-form-item {
  margin-right: 8px ;
  margin-bottom: 8px;
}

.form_session {
  margin-top: 20px;
  margin-bottom: -5px;
  float: right;
}

.chart_session {
  display: flex;
  flex-wrap: wrap;
  width: 100%
}

.chart_item {
  width: 48%;
}

@media (max-width: 1080px) {

.chart_item {
   width: 100%;
 }

}

/* Card */
.dashboard_container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;   
    width: 100%; 
}
.wrimagecard{	
    width: 24%;
    text-align: left;
    position: relative;
    background: #fff;
    box-shadow: 1px 2px 4px 0px rgba(46,61,73,0.2);
    border-radius: 4px;
    transition: all 0.3s ease;
}
.wrimagecard i{
	position: relative;
  font-size: 20px;
  font-weight: 700;
}
.wrimagecard_value {
    float: right;
    font-weight: 700;
}
.wrimagecard-topimage_header{
    padding: 10px;
    background-color:rgba(187, 120, 36, 0.1)
}

.wrimagecard-topimage:hover {
    box-shadow: 0px 1px 2px 0px rgba(46,61,73,0.2);
}

.wrimagecard-topimage_title {
  padding: 10px 12px;
  position: relative;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 1080px) {

.wrimagecard {
   width: 32%;
 }

}

@media (max-width: 630px) {

.wrimagecard {
   width: 48%;
 }

}

@media (max-width: 477px) {

.wrimagecard {
   width: 100%;
 }
 
}
</style>