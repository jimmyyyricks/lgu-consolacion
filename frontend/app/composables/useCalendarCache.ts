/**
 * Calendar Cache Composable
 * =========================
 * Caches API responses for the PM Calendar to reduce redundant API calls.
 * Follows Single Responsibility Principle - handles all caching logic.
 */

import type { PmTask, LaborOption } from "./usePmCalendar"

export const useCalendarCache = () => {
  const { fetchTasks, fetchLabor } = usePmCalendar()

  // ── Cache State ─────────────────────────────────────────────────────────────
  const cachedTasks = ref<Map<string, PmTask[]>>(new Map())
  const cachedLabor = ref<LaborOption[] | null>(null)

  // ── Cache Key Helpers ───────────────────────────────────────────────────────
  const getYearMonthKey = (year: number, month: number): string => {
    return `${year}-${month}`
  }

  // ── Tasks Cache ───────────────────────────────────────────────────────────────
  const getOrFetchTasks = async (year: number, month: number): Promise<PmTask[]> => {
    const key = getYearMonthKey(year, month)
    
    // Return cached if available
    if (cachedTasks.value.has(key)) {
      return cachedTasks.value.get(key)!
    }
    
    // Fetch and cache
    const data = await fetchTasks(year, month)
    cachedTasks.value.set(key, data)
    return data
  }

  // ── Labor Cache ───────────────────────────────────────────────────────────────
  const getOrFetchLabor = async (): Promise<LaborOption[]> => {
    // Return cached if available
    if (cachedLabor.value !== null) {
      return cachedLabor.value
    }
    
    // Fetch and cache
    const data = await fetchLabor()
    cachedLabor.value = data
    return data
  }

  return {
    getOrFetchTasks,
    getOrFetchLabor,
  }
}
