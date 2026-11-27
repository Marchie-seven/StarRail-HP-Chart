import type { Mode, Period } from '../types'
import {
  ApiError,
  fromChartPeriod,
  fromPeriod,
  type ChartQuery,
  type ModeChart,
  type ModeChartDto,
  type PeriodDto,
  type PeriodPage,
  type PeriodPageDto,
  type PeriodQuery,
} from './contracts'

export { ApiError } from './contracts'
export type { ChartPeriod, ChartQuery, ModeChart, PeriodPage, PeriodQuery } from './contracts'

export const API_BASE_URL = 'http://127.0.0.1:8000/api'
const useMock = false

function encodeQuery(query: ChartQuery & Partial<Pick<PeriodQuery, 'mode' | 'page' | 'pageSize'>>) {
  const values = {
    mode: query.mode,
    major_version: query.majorVersion,
    version: query.version,
    half: query.half,
    page: query.page,
    page_size: query.pageSize,
  }
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(values)) {
    if (value !== undefined) params.set(key, String(value))
  }
  return params
}

function responseError(status: number, body: unknown): ApiError {
  const detail = body && typeof body === 'object' && 'detail' in body ? body.detail : undefined
  if (detail && typeof detail === 'object' && 'code' in detail && 'message' in detail
    && typeof detail.code === 'string' && typeof detail.message === 'string') {
    return new ApiError(status, detail.code, detail.message)
  }

  if (status === 422) return new ApiError(status, 'INVALID_QUERY', '期数查询参数无效。')
  if (status === 404) return new ApiError(status, 'NOT_FOUND', '没有找到请求的档案。')
  if ([502, 503, 504].includes(status)) {
    return new ApiError(status, 'SERVICE_UNAVAILABLE', '档案暂时无法加载，请稍后重试。')
  }
  return new ApiError(status, 'HTTP_ERROR', '档案加载失败，请重试。')
}

async function request<T>(path: string, params?: URLSearchParams): Promise<T> {
  const query = params?.toString()
  const url = API_BASE_URL + path + (query ? '?' + query : '')
  let response: Response

  try {
    response = await fetch(url, { headers: { Accept: 'application/json' } })
  } catch {
    throw new ApiError(0, 'NETWORK_ERROR', '无法连接档案服务，请检查网络后重试。')
  }

  const body: unknown = await response.json().catch(() => undefined)
  if (!response.ok) throw responseError(response.status, body)
  if (body === undefined || body === null) {
    throw new ApiError(response.status, 'INVALID_RESPONSE', '档案服务返回了无效数据。')
  }
  return body as T
}

/** GET /api/periods */
export async function getPeriods(query: PeriodQuery): Promise<PeriodPage> {
  const result = useMock
    ? await (await import('./mock')).mockPeriodList(query)
    : await request<PeriodPageDto>('/periods', encodeQuery(query))

  return { items: result.items.map(fromPeriod), page: result.page, pageSize: result.page_size, total: result.total }
}

/** GET /api/periods/{id} */
export async function getPeriodDetail(id: string): Promise<Period> {
  const result = useMock
    ? await (await import('./mock')).mockPeriodDetail(id)
    : await request<PeriodDto>('/periods/' + encodeURIComponent(id))

  return fromPeriod(result)
}

/** GET /api/periods/latest */
export async function getLatestPeriods(): Promise<Period[]> {
  const result = useMock
    ? await (await import('./mock')).mockLatestPeriods()
    : await request<PeriodDto[]>('/periods/latest')

  return result.map(fromPeriod)
}

/** GET /api/modes/{mode}/chart */
export async function getModeChart(mode: Mode, query: ChartQuery = {}): Promise<ModeChart> {
  const result = useMock
    ? await (await import('./mock')).mockModeChart(mode, query)
    : await request<ModeChartDto>('/modes/' + encodeURIComponent(mode) + '/chart', encodeQuery(query))

  return { mode: result.mode, periods: result.periods.map(fromChartPeriod) }
}
