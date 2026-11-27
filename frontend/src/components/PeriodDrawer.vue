<script setup lang="ts">
import { CalendarDays, HeartPulse, X } from '@lucide/vue'
import { onMounted, ref } from 'vue'
import { getPeriodDetail } from '../api'
import { formatDate, formatHp, periodLabel } from '../domain/periods'
import type { Period } from '../types'
import RewardItems from './RewardItems.vue'
import StateMessage from './StateMessage.vue'
import WeaknessTags from './WeaknessTags.vue'

const props = defineProps<{ periodId: string; label: string }>()
const emit = defineEmits<{ close: [] }>()
const dialog = ref<HTMLDialogElement>()
const period = ref<Period>()
const loading = ref(true)
const error = ref('')

async function loadPeriod() {
  loading.value = true
  error.value = ''

  try {
    period.value = await getPeriodDetail(props.periodId)
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : '详情加载失败。'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  dialog.value?.showModal()
  void loadPeriod()
})
</script>

<template>
  <Teleport to="body">
    <dialog ref="dialog" class="drawer" aria-labelledby="period-drawer-title"
      @close="emit('close')" @click.self="dialog?.close()">
      <div class="drawer__inner">
        <header class="drawer__header">
          <div>
            <div class="drawer__eyebrow">期数详情</div>
            <h2 id="period-drawer-title">{{ period ? periodLabel(period) : label }}</h2>
          </div>
          <button type="button" class="icon-button" aria-label="关闭期数详情" autofocus @click="dialog?.close()">
            <X :size="22" />
          </button>
        </header>
        <StateMessage v-if="loading" status="loading" />
        <StateMessage v-else-if="error" status="error" :message="error" @retry="loadPeriod" />
        <div v-else-if="period" class="drawer__body">
          <div class="drawer__summary">
            <div><CalendarDays :size="17" aria-hidden="true" /> {{ formatDate(period.startTime) }} 至 {{ formatDate(period.endTime) }}</div>
            <div><HeartPulse :size="18" aria-hidden="true" /> <strong>{{ formatHp(period.totalHp) }} HP</strong> <span>总血量</span></div>
          </div>
          <section class="drawer__section">
            <h3>怪物阵容 <small>{{ period.monsters.length }} 只</small></h3>
            <p v-if="!period.monsters.length" class="inline-empty">该期暂无阵容记录。</p>
            <ul v-else class="drawer-monsters">
              <li v-for="(monster, index) in period.monsters" :key="index">
                <div class="drawer-monsters__title">
                  <strong>{{ monster.name }}</strong><span>{{ formatHp(monster.hp) }} HP</span>
                </div>
                <div class="drawer-monsters__meta">
                  <span>{{ monster.floor }} · {{ monster.room }}</span>
                  <WeaknessTags :weaknesses="monster.weakness" />
                </div>
                <p v-if="monster.note">{{ monster.note }}</p>
              </li>
            </ul>
          </section>
          <section class="drawer__section">
            <h3>通关奖励</h3>
            <RewardItems :rewards="period.rewards" />
          </section>
        </div>
      </div>
    </dialog>
  </Teleport>
</template>
