<script setup lang="ts">
import { LineChart } from 'echarts/charts'
import { AriaComponent, DataZoomComponent, GridComponent, TooltipComponent } from 'echarts/components'
import { graphic, init, use, type EChartsType } from 'echarts/core'
import { SVGRenderer } from 'echarts/renderers'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { formatHp, periodLabel } from '../domain/periods'
import type { TrendSeries } from '../domain/trends'
import type { Period } from '../types'

use([LineChart, GridComponent, TooltipComponent, DataZoomComponent, AriaComponent, SVGRenderer])

const props = defineProps<{ periods: Period[]; series: TrendSeries[] }>()
const emit = defineEmits<{ select: [period: Period] }>()
const container = ref<HTMLDivElement>()

const compactHp = new Intl.NumberFormat('zh-CN', { notation: 'compact', maximumFractionDigits: 1 })
const gradientEnds = ['#ffce83', '#f8eab2', '#e1b6ff', '#b1f5e4', '#ffd0ae', '#cdc2ff']
let chart: EChartsType | undefined
let observer: ResizeObserver | undefined
let visibleCount = 0

function append(parent: HTMLElement, className: string, content: string) {
  const element = document.createElement('div')
  element.className = className
  element.textContent = content
  parent.append(element)
}

function tooltip(index: number): HTMLElement {
  const wrapper = document.createElement('div')
  wrapper.className = 'chart-tip'
  const period = props.periods[index]
  if (!period) return wrapper

  append(wrapper, 'chart-tip__title', periodLabel(period))
  for (const series of props.series) {
    const point = series.points[index]
    if (!point) continue

    append(wrapper, 'chart-tip__total', series.name + ' · ' + formatHp(point.hp) + ' HP')
    if (!point.monsters.length) append(wrapper, 'chart-tip__meta', '暂无怪物记录')
    for (const monster of point.monsters) {
      append(wrapper, 'chart-tip__monster', monster.name + ' · ' + formatHp(monster.hp) + ' HP')
      const weaknesses = monster.weakness.join('、') || '—'
      append(wrapper, 'chart-tip__meta', monster.floor + ' / ' + monster.room + ' · 弱点 ' + weaknesses)
    }
  }

  return wrapper
}

function render() {
  if (!chart || !container.value) return
  const periods = new Map(props.periods.map(period => [period.id, period]))
  const width = container.value.clientWidth
  const baseFont = 'system-ui, "Microsoft YaHei", sans-serif'
  const textColor = '#cfc2da'
  visibleCount = Math.max(2, Math.min(14, Math.floor((width - 65) / 57)))
  const zoomed = props.periods.length > visibleCount
  const showSlider = props.periods.length > 1

  chart.setOption({
    animation: false,
    backgroundColor: 'transparent',
    color: props.series.map(series => series.color),
    textStyle: { fontFamily: baseFont, color: textColor },
    aria: { enabled: true, label: { description: '按期数排列的怪物血量趋势。可以在下方表格使用键盘打开期数详情。' } },
    grid: { top: 35, bottom: showSlider ? 86 : 50, left: width < 480 ? 51 : 71, right: width < 480 ? 12 : 23 },
    tooltip: {
      trigger: 'axis',
      renderMode: 'html',
      confine: true,
      enterable: true,
      backgroundColor: '#20182efa',
      borderColor: '#a681735e',
      borderWidth: 1,
      padding: 12,
      textStyle: { color: '#fff2e3', fontSize: 13 },
      axisPointer: { type: 'line', lineStyle: { color: '#edb88785', type: 'dashed' } },
      formatter: (raw: unknown) => {
        const params = Array.isArray(raw) ? raw[0] : raw
        return tooltip(params?.dataIndex ?? -1)
      },
    },
    xAxis: {
      type: 'category',
      data: props.periods.map(period => period.id),
      boundaryGap: true,
      axisTick: { show: false },
      axisLine: { lineStyle: { color: '#c6aac34a' } },
      axisLabel: {
        interval: 0,
        color: textColor,
        margin: 12,
        formatter: (key: string) => {
          const period = periods.get(key)
          return period ? '{version|' + period.version + '}\n{half|' + period.half + '}' : ''
        },
        rich: {
          version: { fontSize: 13, fontWeight: 650, lineHeight: 18, color: '#f7e8da', align: 'center' },
          half: { fontSize: 11, lineHeight: 17, color: textColor, align: 'center' },
        },
      },
    },
    yAxis: {
      type: 'value',
      name: 'HP',
      nameTextStyle: { color: textColor, fontSize: 12, align: 'right' },
      scale: true,
      splitNumber: 4,
      minInterval: 1,
      axisLabel: { color: textColor, fontSize: 11, formatter: (value: number) => compactHp.format(value) },
      splitLine: { lineStyle: { color: '#bca4c928' } },
    },
    dataZoom: showSlider ? [
      {
        type: 'inside',
        filterMode: 'none',
        startValue: 0,
        endValue: zoomed ? visibleCount - 1 : props.periods.length - 1,
        zoomOnMouseWheel: 'ctrl',
        moveOnMouseWheel: false,
      },
      {
        type: 'slider',
        filterMode: 'none',
        bottom: 12,
        height: 18,
        left: width < 480 ? 51 : 71,
        right: width < 480 ? 12 : 23,
        backgroundColor: '#18152a',
        borderColor: '#a781736b',
        fillerColor: 'rgba(235, 162, 115, 0.24)',
        handleStyle: { color: '#f6cca6', borderColor: '#d7a47f' },
        moveHandleStyle: { color: '#cfa27c' },
        showDetail: false,
        showDataShadow: false,
        brushSelect: false,
      },
    ] : [],
    series: props.series.map((series, index) => {
      const line = new graphic.LinearGradient(0, 0, 1, 0, [
        { offset: 0, color: series.color },
        { offset: 1, color: gradientEnds[index % gradientEnds.length] },
      ])
      const area = new graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: series.color + '36' },
        { offset: 1, color: series.color + '03' },
      ])
      return {
        type: 'line',
        name: series.name,
        data: series.points.map(point => point?.hp ?? null),
        connectNulls: series.connectNulls ?? false,
        symbol: 'circle',
        symbolSize: width < 480 ? 12 : 9,
        showSymbol: true,
        lineStyle: { width: 2.5, color: line, shadowBlur: 8, shadowColor: series.color + '75' },
        itemStyle: { color: series.color, borderColor: '#fff0d8', borderWidth: 1.4, shadowBlur: 9, shadowColor: series.color },
        emphasis: { focus: 'series' },
        areaStyle: props.series.length === 1 ? { color: area, opacity: 1 } : undefined,
      }
    }),
  }, { notMerge: true })
}

onMounted(() => {
  if (!container.value) return

  chart = init(container.value, 'dark', { renderer: 'svg' })
chart.on('click', event => {
  if (event.componentType !== 'series') return

  const period = props.periods[event.dataIndex]

  console.log('点击的期数：', period)

  if (period) emit('select', period)
})

  render()
  observer = new ResizeObserver(([entry]) => {
    chart?.resize()
    const nextCount = Math.max(2, Math.min(14, Math.floor((entry.contentRect.width - 65) / 57)))
    if (nextCount !== visibleCount) render()
  })
  observer.observe(container.value)
})

watch(() => [props.periods, props.series], render, { flush: 'post' })

onBeforeUnmount(() => {
  observer?.disconnect()
  chart?.dispose()
})
</script>

<template>
  <div ref="container" class="trend-chart" />
</template>
