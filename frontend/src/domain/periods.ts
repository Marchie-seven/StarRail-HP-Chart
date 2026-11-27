import type { Period } from '../types'

const numberFormat = new Intl.NumberFormat('zh-CN')
const dateFormat = new Intl.DateTimeFormat('zh-CN', {
  timeZone: 'Asia/Shanghai',
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
})

export function formatHp(value: number): string {
  return numberFormat.format(value)
}

export function formatDate(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.valueOf())) return '—'

  return dateFormat.format(date).replaceAll('/', '.')
}

export function periodLabel(period: Period): string {
  return period.version + ' ' + period.half
}

export function compareVersions(left: string, right: string): number {
  const [leftMajor, leftMinor] = left.split('.').map(Number)
  const [rightMajor, rightMinor] = right.split('.').map(Number)
  return leftMajor - rightMajor || leftMinor - rightMinor
}

export function comparePeriods(left: Period, right: Period): number {
  return compareVersions(left.version, right.version)
    || Number(left.half === '下半') - Number(right.half === '下半')
}
