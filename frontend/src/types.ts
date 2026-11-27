export const MODES = ['fiction', 'forgotten', 'apocalypse', 'arbitration'] as const
export type Mode = (typeof MODES)[number]
export type Half = '上半' | '下半'

export interface Monster {
  id: string
  name: string
  hp: number
  weakness: string[]
  floor: string
  room: string
  note?: string
}

export interface Reward {
  name: string
  icon?: string
  amount: number
  condition: string
}

export interface Period {
  id: string
  mode: Mode
  majorVersion: number
  version: string
  half: Half
  startTime: string
  endTime: string
  monsters: Monster[]
  rewards: Reward[]
  totalHp: number
}
