<script setup lang="ts">
import { Coins, Footprints, Gem, Gift, Medal, Droplet } from '@lucide/vue'
import type { Component } from 'vue'
import { formatHp } from '../domain/periods'
import type { Reward } from '../types'

defineProps<{ rewards: Reward[] }>()

const icons: ReadonlyMap<string, Component> = new Map([
  ['stellar-jade', Gem],
  ['credits', Coins],
  ['medal', Medal],
  ['resin', Droplet],
  ['tracks', Footprints],
])
</script>

<template>
  <ul v-if="rewards.length" class="reward-list">
    <li v-for="(reward, index) in rewards" :key="index" class="reward-item">
      <span class="reward-item__icon" aria-hidden="true">
        <component :is="icons.get(reward.icon ?? '') ?? Gift" :size="22" :stroke-width="1.7" />
      </span>
      <div class="reward-item__body">
        <strong>{{ reward.name }}</strong>
        <small>{{ reward.condition }}</small>
      </div>
      <span class="reward-item__amount">× {{ formatHp(reward.amount) }}</span>
    </li>
  </ul>
  <p v-else class="inline-empty">该期暂无奖励记录。</p>
</template>
