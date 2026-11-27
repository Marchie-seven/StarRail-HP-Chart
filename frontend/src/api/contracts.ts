import type { Half, Mode, Monster, Period, Reward } from '../types'

export interface ChartQuery {
  majorVersion?: number
  version?: string
  half?: Half
}

export interface PeriodQuery extends ChartQuery {
  mode: Mode
  page?: number
  pageSize?: number
}

export interface PeriodPage {
  items: Period[]
  page: number
  pageSize: number
  total: number
}

export type ChartPeriod = Omit<Period, 'rewards'>

export interface ModeChart {
  mode: Mode
  periods: ChartPeriod[]
}

export type MonsterDto = Omit<Monster, 'note'> & { note?: string | null }
export type RewardDto = Omit<Reward, 'icon'> & { icon?: string | null }

export interface ChartPeriodDto {
  id: string
  mode: Mode
  major_version: number
  version: string
  half: Half
  start_time: string
  end_time: string
  monsters: MonsterDto[]
  total_hp: number
}

export interface PeriodDto extends ChartPeriodDto {
  rewards: RewardDto[]
}

export interface PeriodPageDto {
  items: PeriodDto[]
  page: number
  page_size: number
  total: number
}

export interface ModeChartDto {
  mode: Mode
  periods: ChartPeriodDto[]
}

export class ApiError extends Error {
  constructor(readonly status: number, readonly code: string, message: string) {
    super(message)
    this.name = 'ApiError'
  }
}

export function fromChartPeriod(period: ChartPeriodDto): ChartPeriod {
  return {
    id: period.id,
    mode: period.mode,
    majorVersion: period.major_version,
    version: period.version,
    half: period.half,
    startTime: period.start_time,
    endTime: period.end_time,
    monsters: period.monsters.map(({ note, ...monster }) => ({ ...monster, note: note ?? undefined })),
    totalHp: period.total_hp,
  }
}

export function fromPeriod(period: PeriodDto): Period {
  return {
    ...fromChartPeriod(period),
    rewards: period.rewards.map(({ icon, ...reward }) => ({ ...reward, icon: icon ?? undefined })),
  }
}
