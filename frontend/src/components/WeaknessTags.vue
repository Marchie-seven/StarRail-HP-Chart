<script setup lang="ts">
defineProps<{ weaknesses: string[] }>()

const palette: Readonly<Record<string, string>> = {
  物理: 'physical',
  火: 'fire',
  冰: 'ice',
  雷: 'lightning',
  风: 'wind',
  量子: 'quantum',
  虚数: 'imaginary',
}
</script>

<template>
  <span v-if="weaknesses.length" class="weaknesses">
    <span v-for="(weakness, index) in weaknesses" :key="index" class="weakness"
      :class="'weakness--' + (palette[weakness] ?? 'physical')">
      {{ weakness }}
    </span>
  </span>
  <span v-else aria-label="暂无弱点数据">—</span>
</template>
