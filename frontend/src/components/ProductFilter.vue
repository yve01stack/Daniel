<template>
  <div style="opacity: 0.7;">
    <h3><i style="font-size: medium;" class="far fa-filter"></i> Filtre</h3>
    <el-form  :inline="true" :model="formSearch">
      <el-form-item>
        <el-input
          v-model="formSearch.query"
          placeholder="Rechercher..."
          :prefix-icon="Search"
        />
      </el-form-item>
      <el-form-item>
        <el-select
          v-model="selectedCategories"
          multiple
          clearable
          collapse-tags
          placeholder="Catégorie"
          popper-class="custom-header"
          :max-collapse-tags="1"
        >
          <template #header>
            <el-checkbox v-model="checkAll" @change="handleCheckAll">Tout</el-checkbox>
          </template>
          <el-option
            v-for="item in categories"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select
          v-model="formSearch.available_in"
          multiple
          collapse-tags
          placeholder="Disponible"
        >
          <el-option
            v-for="item in availabilities"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select v-model="formSearch.sortBy"
        placeholder="Trier par" style="min-width: 160px;">
          <el-option
            v-for="item in sortBy"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
      </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">Rechercher</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, ref, watch, defineProps, defineEmits } from 'vue'
import { Search } from '@element-plus/icons-vue'

const emit = defineEmits(['queryData']);

const props = defineProps({
  categories: {type: Object, required: true},
  availabilities: {type: Object, required: true},
});

const checkAll = ref(false);
const selectedCategories = ref([]);
const categories = ref(props.categories);
const sortBy = [
  {
    value: 'price',
    label: 'Prix',
  },
  {
    value: 'rating',
    label: 'Notation',
  },
];

const handleCheckAll = () => {
  if (checkAll.value) {
    selectedCategories.value = categories.value.map(category => category.value);
  } else {
    selectedCategories.value = [];
  }
};

watch(selectedCategories, (newVal) => {
  checkAll.value = newVal.length === categories.value.length;
});

const formSearch = reactive({
  query: '',
  category: [],
  available_in: [],
  sortBy: '',
})

const submitForm = () => {
  formSearch.category = selectedCategories.value;
  emit('queryData', formSearch);
};

</script>

<style lang="scss" scoped>
.custom-header {
  .el-checkbox {
    display: flex;
    height: unset;
  }
}

.el-form--inline .el-form-item {
  margin-right: 8px ;
  margin-bottom: 8px;
}

.el-form--inline .el-form-item .el-input {
  width: 160px;
}

.el-form--inline .el-form-item .el-select {
  min-width: 160px;
}

</style>
