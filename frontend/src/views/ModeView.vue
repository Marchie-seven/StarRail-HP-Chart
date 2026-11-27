
<script setup lang="ts">
import { Activity, CalendarDays, ChevronDown, ChartNoAxesCombined, Gift, Layers3, Table2 } from '@lucide/vue'
import { computed, onMounted, ref, watch } from 'vue'
import { getModeChart, getPeriods } from '../api'
import PeriodDrawer from '../components/PeriodDrawer.vue'
import PeriodTable from '../components/PeriodTable.vue'
import RewardItems from '../components/RewardItems.vue'
import StateMessage from '../components/StateMessage.vue'
import TrendChart from '../components/TrendChart.vue'
import { modeInfo } from '../domain/modes'
import { comparePeriods, compareVersions, formatHp, periodLabel } from '../domain/periods'
import { monsterPoint, trendColors, type TrendSeries } from '../domain/trends'
import type { Mode, Period } from '../types'

const props = defineProps<{ mode: Mode }>()
const info = computed(() => modeInfo[props.mode])

const loading = ref(true)
const error = ref('')
const periods = ref<Period[]>([])

// 第四个接口专门返回图表数据
const chartPeriods = ref<Period[]>([])
const chartLoading = ref(false)
const chartError = ref('')
let chartRequestId = 0

const majorVersion = ref<number | ''>('')
const minorVersion = ref('')

const metrics = [
  { id: 'total', label: '每期总血量' },
  { id: 'monster', label: '单个怪物' },
  { id: 'floor', label: '某一层' },
] as const

const metric = ref<(typeof metrics)[number]['id']>('total')
const compareHalves = ref(false)
const selectedMonsters = ref<string[]>([])
const floor = ref('')
const rewardPeriodId = ref('')
const openedPeriod = ref<Period>()

async function loadHistory() {
  loading.value = true
  error.value = ''

  try {
    const collected: Period[] = []
    const mode = props.mode
    let page = 1

    while (true) {
      const result = await getPeriods({ mode, page, pageSize: 100 })
      collected.push(...result.items)

      if (result.page * result.pageSize >= result.total || result.items.length === 0) break

      page = result.page + 1
    }

    periods.value = collected.sort(comparePeriods)
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : '玩法档案加载失败。'
  } finally {
    loading.value = false
  }
}

const majors = computed(() =>
  [...new Set(periods.value.map(period => period.majorVersion))]
    .sort((a, b) => a - b)
)

const minors = computed(() =>
  [...new Set(periods.value
    .filter(period => majorVersion.value === '' || period.majorVersion === majorVersion.value)
    .map(period => period.version))]
    .sort(compareVersions)
)

const filtered = computed(() => periods.value.filter(period => (
  (majorVersion.value === '' || period.majorVersion === majorVersion.value)
  && (!minorVersion.value || period.version === minorVersion.value)
)))

const lastPeriod = computed(() => filtered.value.reduce<Period | undefined>((latest, item) => {
  if (!latest || Date.parse(item.startTime) >= Date.parse(latest.startTime)) return item
  return latest
}, undefined))

const peakHp = computed(() =>
  filtered.value.reduce((max, period) => Math.max(max, period.totalHp), 0)
)

const monsterOptions = computed(() =>
  Array.from(new Map(filtered.value
    .flatMap(period => period.monsters.map(monster => [monster.id, monster.name] as const))))
)

const floorOptions = computed(() =>
  [...new Set(filtered.value.flatMap(period => period.monsters.map(monster => monster.floor)))]
    .sort((a, b) => a.localeCompare(b, 'zh-CN', { numeric: true }))
)

const rewardPeriod = computed(() =>
  filtered.value.find(period => period.id === rewardPeriodId.value)
)

// 请求第四个接口，获取图表数据
async function loadChart() {
  const requestId = ++chartRequestId

  chartError.value = ''

  // 后端目前要求 major_version 和 version 都必须传递。
  // 如果没有选择具体小版本，暂时使用原来的本地筛选数据。
  if (!minorVersion.value) {
    chartPeriods.value = filtered.value
    chartLoading.value = false
    return
  }

  // 小版本格式为 2.2。
  // 如果没有选择大版本，就从完整版本号中提取。
  const selectedMajor = majorVersion.value !== ''
    ? majorVersion.value
    : Number(minorVersion.value.split('.')[0])

  if (!Number.isInteger(selectedMajor)) {
    chartPeriods.value = filtered.value
    return
  }

  chartLoading.value = true

  try {
    const result = await getModeChart(props.mode, {
      majorVersion: selectedMajor,
      version: minorVersion.value,
    })

    // 防止较早发出的请求覆盖最新筛选结果
    if (requestId !== chartRequestId) return

    // 图表接口不返回 rewards。
    // 从原来的期数数据中补充 rewards，
    // 让 TrendChart 继续使用原来的 Period 类型。
    chartPeriods.value = result.periods.map(chartPeriod => {
      const originalPeriod = periods.value.find(
        period => period.id === chartPeriod.id
      )

      return {
        ...chartPeriod,
        rewards: originalPeriod?.rewards ?? [],
      }
    }).sort(comparePeriods)

  } catch (cause) {
    if (requestId !== chartRequestId) return

    chartError.value = cause instanceof Error
      ? cause.message
      : '血量趋势加载失败。'

    chartPeriods.value = []
  } finally {
    if (requestId === chartRequestId) {
      chartLoading.value = false
    }
  }
}

// 版本变化时重新获取图表数据
watch([majorVersion, minorVersion], () => {
  void loadChart()
})

watch(minors, options => {
  if (minorVersion.value && !options.includes(minorVersion.value)) {
    minorVersion.value = ''
  }
}, { flush: 'sync' })

watch(monsterOptions, options => {
  const valid = new Set(options.map(([id]) => id))
  const retained = selectedMonsters.value.filter(id => valid.has(id))
  selectedMonsters.value = retained.length > 0
    ? retained
    : options.slice(0, 1).map(([id]) => id)
})

watch(floorOptions, options => {
  if (!options.includes(floor.value)) {
    floor.value = options[0] ?? ''
  }
})

watch(filtered, options => {
  if (!options.some(period => period.id === rewardPeriodId.value)) {
    rewardPeriodId.value = lastPeriod.value?.id ?? ''
  }
})

// 切换玩法时重新获取数据
watch(() => props.mode, async () => {
  majorVersion.value = ''
  minorVersion.value = ''
  chartRequestId++

  await loadHistory()
  await loadChart()
})

const series = computed<TrendSeries[]>(() => {
  if (metric.value === 'monster') {
    return monsterOptions.value
      .filter(([id]) => selectedMonsters.value.includes(id))
      .map(([id, name], index) => ({
        name,
        color: trendColors[index % trendColors.length],
        points: chartPeriods.value.map(period =>
          monsterPoint(period, monster => monster.id === id)
        ),
      }))
  }

  if (metric.value === 'floor') {
    if (!floor.value) return []

    return [{
      name: floor.value + '总血量',
      color: trendColors[0],
      points: chartPeriods.value.map(period =>
        monsterPoint(period, monster => monster.floor === floor.value)
      ),
    }]
  }

  if (compareHalves.value) {
    return (['上半', '下半'] as const).map((half, index) => ({
      name: half + '总血量',
      color: trendColors[index],
      points: chartPeriods.value.map(period =>
        period.half === half
          ? { hp: period.totalHp, monsters: period.monsters }
          : null
      ),
      connectNulls: true,
    }))
  }

  return [{
    name: '每期总血量',
    color: trendColors[0],
    points: chartPeriods.value.map(period => ({
      hp: period.totalHp,
      monsters: period.monsters,
    })),
  }]
})

const hasPoints = computed(() =>
  series.value.some(line => line.points.some(point => point !== null))
)

onMounted(async () => {
  await loadHistory()
  await loadChart()
})
</script>

<template>
  <div class="mode-page">
    <nav class="breadcrumb" aria-label="当前位置">
      <RouterLink :to="{ name: 'home' }">首页</RouterLink>
      <span aria-hidden="true">/</span>
      <span aria-current="page">{{ info.name }}</span>
    </nav>

    <div class="mode-heading" :style="{ '--mode-color': info.color, '--mode-tint': info.tint }">
      <span class="mode-symbol mode-symbol--large" aria-hidden="true">
        <component :is="info.icon" :size="30" :stroke-width="1.6" />
      </span>
      <div>
        <h1>{{ info.name }}</h1>
        <p>{{ info.description }}</p>
      </div>
    </div>

    <div v-if="loading || error || !periods.length" class="panel mode-state">
      <StateMessage v-if="loading" status="loading" />
      <StateMessage v-else-if="error" status="error" :message="error" @retry="loadHistory" />
      <StateMessage v-else status="empty" message="该玩法暂无期数记录。" />
    </div>

    <template v-else>
      <div class="stat-grid" aria-label="筛选结果概览">
        <div class="panel stat">
          <span class="stat__icon"><Layers3 :size="20" /></span>
          <div><span>收录期数</span><strong>{{ filtered.length }} <small>期</small></strong></div>
        </div>
        <div class="panel stat">
          <span class="stat__icon"><Activity :size="20" /></span>
          <div><span>最高总血量</span><strong>{{ filtered.length ? formatHp(peakHp) : '—' }} <small v-if="filtered.length">HP</small></strong></div>
        </div>
        <div class="panel stat">
          <span class="stat__icon"><CalendarDays :size="20" /></span>
          <div><span>最新一期</span><strong>{{ lastPeriod ? periodLabel(lastPeriod) : '—' }}</strong></div>
        </div>
      </div>

      <section class="panel chart-panel" aria-labelledby="trend-heading">
        <div class="panel-heading">
          <div class="panel-heading__title">
            <ChartNoAxesCombined :size="22" aria-hidden="true" />
            <h2 id="trend-heading">血量趋势</h2>
          </div>

          <div class="period-filters">
            <label class="select-field">
              <span>大版本</span>
              <span class="select-wrap">
                <select v-model="majorVersion">
                  <option value="">全部</option>
                  <option v-for="major in majors" :key="major" :value="major">
                    {{ major }}.x
                  </option>
                </select>
                <ChevronDown :size="15" aria-hidden="true" />
              </span>
            </label>

            <label class="select-field">
              <span>小版本</span>
              <span class="select-wrap">
                <select v-model="minorVersion">
                  <option value="">全部</option>
                  <option v-for="minor in minors" :key="minor" :value="minor">
                    {{ minor }}
                  </option>
                </select>
                <ChevronDown :size="15" aria-hidden="true" />
              </span>
            </label>
          </div>
        </div>

        <div class="chart-controls">
          <div class="segmented" role="group" aria-label="统计口径">
            <button
              v-for="item in metrics"
              :key="item.id"
              type="button"
              :aria-pressed="metric === item.id"
              @click="metric = item.id"
            >
              {{ item.label }}
            </button>
          </div>

          <label v-if="metric === 'total'" class="check-control">
            <input v-model="compareHalves" type="checkbox" /> 上半 / 下半对比
          </label>

          <fieldset v-else-if="metric === 'monster' && monsterOptions.length" class="monster-options">
            <legend>选择怪物，可多选</legend>
            <div class="monster-options__items">
              <label v-for="[id, name] in monsterOptions" :key="id" class="check-control">
                <input v-model="selectedMonsters" type="checkbox" :value="id" />
                {{ name }}
              </label>
            </div>
          </fieldset>

          <label v-else-if="metric === 'floor' && floorOptions.length" class="select-field">
            <span>选择层级</span>
            <span class="select-wrap">
              <select v-model="floor">
                <option v-for="item in floorOptions" :key="item" :value="item">
                  {{ item }}
                </option>
              </select>
              <ChevronDown :size="15" aria-hidden="true" />
            </span>
          </label>
        </div>

        <StateMessage
          v-if="chartLoading"
          status="loading"
        />

        <StateMessage
          v-else-if="chartError"
          status="error"
          :message="chartError"
          @retry="loadChart"
        />

        <template v-else-if="hasPoints">
          <TrendChart
            :periods="chartPeriods"
            :series="series"
            @select="openedPeriod = $event"
          />

          <div class="chart-footer">
            <ul class="chart-legend" aria-label="图例">
              <li v-for="(line, index) in series" :key="index">
                <i :style="{ '--series-color': line.color }"></i>
                {{ line.name }}
              </li>
            </ul>
            <span>点击数据点查看期数详情</span>
          </div>
        </template>

        <StateMessage
          v-else
          status="empty"
          :message="metric === 'monster' && monsterOptions.length
            ? '请选择至少一只怪物。'
            : '当前筛选没有可绘制的血量记录。'"
        />
      </section>

      <section class="panel table-panel" aria-labelledby="table-heading">
        <div class="panel-heading">
          <div class="panel-heading__title">
            <Table2 :size="22" aria-hidden="true" />
            <h2 id="table-heading">历期怪物明细</h2>
          </div>
          <div class="table-meta">
            <span v-if="filtered.length" class="table-pan-note">左右滑动查看完整明细</span>
            <span class="section-meta">{{ filtered.length }} 期</span>
          </div>
        </div>

        <PeriodTable
          v-if="filtered.length"
          :periods="filtered"
          @select="openedPeriod = $event"
        />
        <StateMessage v-else status="empty" message="当前筛选暂无明细。" />
      </section>

      <section class="panel rewards-panel" aria-labelledby="rewards-heading">
        <div class="panel-heading">
          <div class="panel-heading__title">
            <Gift :size="22" aria-hidden="true" />
            <h2 id="rewards-heading">通关奖励</h2>
          </div>

          <label v-if="filtered.length" class="select-field">
            <span>查看期数</span>
            <span class="select-wrap">
              <select v-model="rewardPeriodId">
                <option v-for="period in filtered" :key="period.id" :value="period.id">
                  {{ periodLabel(period) }}
                </option>
              </select>
              <ChevronDown :size="15" aria-hidden="true" />
            </span>
          </label>
        </div>

        <div v-if="rewardPeriod" class="rewards-panel__content">
          <RewardItems :rewards="rewardPeriod.rewards" />
        </div>
        <StateMessage v-else status="empty" message="当前筛选暂无奖励。" />
      </section>
    </template>

    <PeriodDrawer
      v-if="openedPeriod"
      :key="openedPeriod.id"
      :period-id="openedPeriod.id"
      :label="periodLabel(openedPeriod)"
      @close="openedPeriod = undefined"
    />
  </div>
</template>
