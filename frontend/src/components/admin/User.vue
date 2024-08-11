<template>
    <el-table 
    :data="displayedUsers" 
    :default-sort="{ prop: 'created_on', order: 'descending' }"
    style="width: 100%">
        <el-table-column fixed prop="created_on" label="Date" width="100" sortable  />
        <el-table-column prop="name" width="180">
            <template #header>
                <el-input v-model="search" size="small" placeholder="Type to search" />
            </template>
        </el-table-column>
        <el-table-column prop="status" width="100">
            <template #header>
                <el-button-group class="ml-4">
                    <el-button :icon="ArrowLeft" size="small" @click="prevPage" :disabled="currentPage === 1" />
                    <el-button :icon="ArrowRight" size="small" @click="nextPage" :disabled="currentPage === totalPages" />
                </el-button-group>
            </template>
        </el-table-column>
        <el-table-column prop="email" label="E-mail" width="200" />
        <el-table-column prop="phone" label="Téléphone" width="140" />
        <el-table-column prop="location" label="Adresse" width="280" />
      <el-table-column fixed="right" label="Opérations" min-width="140">
        <template #default="scope">
          <el-button link type="primary" size="small" @click="handleClick(scope.$index, scope.row)">Détails</el-button>
          <el-button link type="primary" size="small">Modifier</el-button>
        </template>
      </el-table-column>
    </el-table>

</template>
  
<script setup>
import { computed, ref, onMounted  } from 'vue';
import { useStore } from 'vuex';
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'

const store = useStore()

const dashboard = computed(() => store.getters['admin/dashboard']);

const search = ref('')
const filterTableData = computed(() =>
    dashboard.value.users.filter(
        (data) =>
        !search.value ||
        data.name.toLowerCase().includes(search.value.toLowerCase())
    )
)

const handleClick = (index, row) => {
    console.log(index, row)
}

const fetchDashboard = async () => {
    await store.dispatch('admin/fetchDashboard');
};

const currentPage = ref(1);
const pageSize = 20;

const totalPages = computed(() => Math.ceil(filterTableData.value.length / pageSize));

const displayedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return filterTableData.value.slice(start, end);
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
    fetchDashboard();
}); 

</script>

<style scoped>

</style>
  