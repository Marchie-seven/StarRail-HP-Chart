<script setup lang="ts">
import { Activity, Orbit } from '@lucide/vue'
import { onMounted, ref } from 'vue'
import { getLatestPeriods } from '../api'
import StateMessage from '../components/StateMessage.vue'
import { modeInfo } from '../domain/modes'
import { formatDate, formatHp, periodLabel } from '../domain/periods'
import { MODES, type Period } from '../types'

const loading = ref(true)
const error = ref('')
const latest = ref<Period[]>([])

async function loadLatest() {
  loading.value = true
  error.value = ''

  try {
    latest.value = await getLatestPeriods()
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : '最新一期加载失败。'
  } finally {
    loading.value = false
  }
}

function showModes() {
  const target = document.getElementById('modes')
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  target?.scrollIntoView({ behavior: reducedMotion ? 'instant' : 'smooth', block: 'start' })
  target?.focus({ preventScroll: true })
}

onMounted(loadLatest)
</script>

<template>
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero__content">
      <div class="hero__eyebrow"><Orbit :size="17" /> 崩坏：星穹铁道</div>
      <h1 id="hero-title">怪物血量<span>统计档案</span></h1>
      <p>比较历期怪物血量，查阅敌方阵容、弱点与奖励。</p>
      <button class="button hero__button" type="button" @click="showModes">浏览玩法</button>
    </div>
  </section>

  <section id="modes" class="home-section" aria-labelledby="modes-title" tabindex="-1">
    <div class="section-heading">
      <div>
        <h2 id="modes-title">玩法档案</h2>
      </div>
    </div>
    <div class="mode-grid">
      <RouterLink v-for="mode in MODES" :key="mode" class="mode-card" :to="{ name: mode }"
        :style="{ '--mode-color': modeInfo[mode].color, '--mode-tint': modeInfo[mode].tint }">
        <span class="mode-symbol" aria-hidden="true"><component :is="modeInfo[mode].icon" :size="24" :stroke-width="1.7" /></span>
        <h3>{{ modeInfo[mode].name }}</h3>
        <p>{{ modeInfo[mode].description }}</p>
        <span class="mode-card__action">查看统计</span>
      </RouterLink>
    </div>
  </section>

  <section class="home-section latest-section" aria-labelledby="latest-title">
    <div class="section-heading">
      <div>
        <h2 id="latest-title">最新一期概览</h2>
        <p>各玩法最近开放一期的总血量与阵容规模。</p>
      </div>
      <Activity class="section-icon" :size="23" aria-hidden="true" />
    </div>
    <div class="panel">
      <StateMessage v-if="loading" status="loading" />
      <StateMessage v-else-if="error" status="error" :message="error" @retry="loadLatest" />
      <StateMessage v-else-if="!latest.length" status="empty" message="暂无最新一期记录。" />
      <div v-else class="latest-grid">
        <RouterLink v-for="period in latest" :key="period.id" class="latest-card" :to="{ name: period.mode }">
          <div class="latest-card__top">
            <strong>{{ modeInfo[period.mode].name }}</strong>
            <span class="phase">{{ periodLabel(period) }}</span>
          </div>
          <span class="latest-card__hp">{{ formatHp(period.totalHp) }} <small>HP</small></span>
          <div class="latest-card__meta"><span>{{ period.monsters.length }} 只怪物</span><time :datetime="period.startTime">{{ formatDate(period.startTime) }} 开放</time></div>
        </RouterLink>
      </div>
    </div>
  </section>
</template>
