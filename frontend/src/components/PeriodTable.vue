<script setup lang="ts">
import { formatDate, formatHp, periodLabel } from '../domain/periods'
import type { Period } from '../types'
import WeaknessTags from './WeaknessTags.vue'

defineProps<{ periods: Period[] }>()
defineEmits<{ select: [period: Period] }>()
</script>

<template>
  <div class="table-scroll" tabindex="0" role="region" aria-label="可横向滚动的历期怪物明细">
    <table class="period-table">
      <caption class="sr-only">每期怪物血量、关卡、弱点和特殊机制</caption>
      <thead>
        <tr>
          <th scope="col">期数</th>
          <th scope="col">怪物名称</th>
          <th scope="col" class="table-hp">血量</th>
          <th scope="col">大版本</th>
          <th scope="col">开放时间</th>
          <th scope="col">关卡 / 节点</th>
          <th scope="col">弱点</th>
          <th scope="col">特殊机制</th>
        </tr>
      </thead>
      <tbody v-for="period in periods" :key="period.id">
        <tr v-for="(monster, index) in period.monsters.length ? period.monsters : [null]" :key="index">
          <th v-if="index === 0" scope="rowgroup" :rowspan="period.monsters.length || 1">
            <button type="button" class="text-button" @click="$emit('select', period)">{{ periodLabel(period) }}</button>
          </th>
          <td class="monster-name">{{ monster?.name ?? '—' }}</td>
          <td class="table-hp">{{ monster ? formatHp(monster.hp) : '—' }}</td>
          <template v-if="index === 0">
            <td :rowspan="period.monsters.length || 1">{{ period.majorVersion }}.x</td>
            <td :rowspan="period.monsters.length || 1" class="table-date">
              <time :datetime="period.startTime">{{ formatDate(period.startTime) }}</time>
              <span>至 <time :datetime="period.endTime">{{ formatDate(period.endTime) }}</time></span>
            </td>
          </template>
          <template v-if="monster">
            <td>{{ monster.floor }} <span class="table-room">{{ monster.room }}</span></td>
            <td><WeaknessTags :weaknesses="monster.weakness" /></td>
            <td class="table-note">{{ monster.note || '—' }}</td>
          </template>
          <td v-else colspan="3" class="table-note">该期暂无阵容记录</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
