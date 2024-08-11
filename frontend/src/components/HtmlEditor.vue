<template>
    <div
      contenteditable="true"
      @input="updateContent"
      :innerHTML="content"
      class="editable-div customScrollbar"
    ></div>
    <el-button size="small" type="danger" @click="save">Enrégistrer</el-button>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue';
  
  const props = defineProps({
    modelValue: {
      type: String,
      default: ''
    }
  });
  const emit = defineEmits(['update:modelValue']);
  
  const content = ref(props.modelValue);
  
  watch(() => props.modelValue, (newValue) => {
    content.value = newValue;
  });
  
  const contentForm = ref('') 

  const updateContent = (event) => {
    contentForm.value = event.target.innerHTML;
  };

  const save = () => {
    emit('update:modelValue', contentForm.value);
  };
  </script>
  
  <style scoped>
  .editable-div {
    border: 1px solid #ccc;
    padding: 10px;
    min-height: 150px;
    cursor: text;
    overflow-y: auto;
    max-height: 300px;
    width: 100%;
  }

  .editable-div:focus {
    border: 1px solid hsl(195, 100%, 63%);
    outline: none; 
  }

  </style>
  