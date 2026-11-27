<script setup lang="ts">
import { CircleAlert, Inbox, LoaderCircle } from '@lucide/vue'

defineProps<{
  status: 'loading' | 'empty' | 'error'
  message?: string
}>()
defineEmits<{ retry: [] }>()
</script>

<template>
  <div class="state-message" :role="status === 'error' ? 'alert' : 'status'">
    <LoaderCircle v-if="status === 'loading'" class="spin" :size="25" />
    <Inbox v-else-if="status === 'empty'" :size="25" />
    <CircleAlert v-else :size="25" />
    <p>{{ message ?? (status === 'loading' ? '正在读取档案…' : status === 'empty' ? '暂无档案数据' : '档案加载失败') }}</p>
    <button v-if="status === 'error'" class="button button--secondary" type="button" @click="$emit('retry')">重试</button>
  </div>
</template>
