import { comparePeriods } from '../domain/periods'
import { mockPeriods } from '../mock/periods'
import { MODES, type Mode, type Period } from '../types'
import {
  ApiError,
  type ChartPeriodDto,
  type ChartQuery,
  type ModeChartDto,
  type PeriodDto,
  type PeriodPageDto,
  type PeriodQuery,
} from './contracts'

async function readMock(): Promise<Period[]> {
  await new Promise<void>(resolve => setTimeout(resolve, 240))

  if (import.meta.env.VITE_MOCK_STATE === 'error') {
    throw new ApiError(503, 'SERVICE_UNAVAILABLE', '档案暂时无法加载，请稍后重试。')
  }

  return import.meta.env.VITE_MOCK_STATE === 'empty' ? [] : mockPeriods
}

function invalidQuery(): never {
  throw new ApiError(422, 'INVALID_QUERY', '期数查询参数无效。')
}

function toChartPeriod(period: Period): ChartPeriodDto {
  return {
    id: period.id,
    mode: period.mode,
    major_version: period.majorVersion,
    version: period.version,
    half: period.half,
    start_time: period.startTime,
    end_time: period.endTime,
    monsters: period.monsters,
    total_hp: period.totalHp,
  }
}

function toPeriod(period: Period): PeriodDto {
  return { ...toChartPeriod(period), rewards: period.rewards }
}

async function findPeriods(mode: Mode, query: ChartQuery): Promise<Period[]> {
  const { majorVersion, version, half } = query
  const versionMajor = version === undefined ? undefined : Number(version.split('.')[0])

  if (
    !MODES.includes(mode)
    || (majorVersion !== undefined && (!Number.isSafeInteger(majorVersion) || majorVersion < 1))
    || (version !== undefined && (!/^[1-9]\d*\.[1-7]$/.test(version) || !Number.isSafeInteger(versionMajor)))
    || (majorVersion !== undefined && versionMajor !== undefined && majorVersion !== versionMajor)
    || (half !== undefined && half !== '上半' && half !== '下半')
  ) invalidQuery()

  const periods = await readMock()
  return periods.filter(period => period.mode === mode
    && (majorVersion === undefined || period.majorVersion === majorVersion)
    && (version === undefined || period.version === version)
    && (half === undefined || period.half === half)
  ).sort(comparePeriods)
}

export async function mockPeriodList(query: PeriodQuery): Promise<PeriodPageDto> {
  const { mode, page = 1, pageSize = 20 } = query

  if (!Number.isSafeInteger(page) || page < 1
    || !Number.isSafeInteger(pageSize) || pageSize < 1 || pageSize > 100) invalidQuery()

  const periods = await findPeriods(mode, query)
  const offset = (page - 1) * pageSize
  const items = periods.slice(offset, offset + pageSize).map(toPeriod)
  return { items: structuredClone(items), page, page_size: pageSize, total: periods.length }
}

export async function mockPeriodDetail(id: string): Promise<PeriodDto> {
  const periods = await readMock()
  const period = periods.find(item => item.id === id)
  if (!period) throw new ApiError(404, 'PERIOD_NOT_FOUND', '没有找到该期档案。')
  return structuredClone(toPeriod(period))
}

export async function mockLatestPeriods(): Promise<PeriodDto[]> {
  const periods = await readMock()
  const latest = MODES.flatMap(mode =>
    periods.filter(period => period.mode === mode)
      .sort((a, b) => Date.parse(b.startTime) - Date.parse(a.startTime) || comparePeriods(b, a))
      .slice(0, 1),
  )

  return structuredClone(latest.map(toPeriod))
}

export async function mockModeChart(mode: Mode, query: ChartQuery): Promise<ModeChartDto> {
  const periods = await findPeriods(mode, query)
  return { mode, periods: structuredClone(periods.map(toChartPeriod)) }
}
