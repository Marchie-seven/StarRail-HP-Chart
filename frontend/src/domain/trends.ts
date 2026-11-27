import type { Monster, Period } from '../types'

export interface TrendPoint {
  hp: number
  monsters: Monster[]
}

export interface TrendSeries {
  name: string
  color: string
  points: (TrendPoint | null)[]
  connectNulls?: boolean
}

export const trendColors = ['#ffab72', '#ecd07b', '#bc9cff', '#8bdfd8', '#f095bc', '#98b9ff']

export function monsterPoint(period: Period, matches: (monster: Monster) => boolean): TrendPoint | null {
  const monsters = period.monsters.filter(matches)
  if (!monsters.length) return null

  return { hp: monsters.reduce((total, monster) => total + monster.hp, 0), monsters }
}
