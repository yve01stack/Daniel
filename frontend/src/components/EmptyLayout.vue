<template>
    <el-empty :description="message" />
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    message: { type: String, required: true },
});
</script>