/**
 * PM Calendar API Composable
 * ===========================
 * All API calls for the Preventive Maintenance Calendar feature.
 */

export interface PmTask {
  id: string
  activity_name: string
  workflow_state: string
  asset_workflow_state: string
  due_date: string
  start_time: string
  laborer: string
  assigned_to: string | null
  assigned_to_name?: string | null
  work_order_activity_id: string | null
  planned_maintenance_activity: string | null
  plan_id: string | null
  asset_id: string | null
  asset_display_name: string | null
  site: string | null
  site_name?: string | null
  department: string | null
  department_name?: string | null
  notes: string | null
  color: string
}

export interface PlanActivity {
  id: string | null
  activity_name: string
  scheduling_type: 'calendar' | 'interval' | 'none'
  frequency: string | null
  interval: number | null
  interval_unit_of_measure_name: string | null
}

export interface LaborOption {
  id: string
  laborer: string
  labor_type: string
}

export const usePmCalendar = () => {
  const { apiFetch, baseURL } = useApiFetch()

  const fetchTasks = async (year: number, month: number, site?: string, department?: string): Promise<PmTask[]> => {
    const params = new URLSearchParams({ year: String(year), month: String(month) })
    if (site) params.set('site', site)
    if (department) params.set('department', department)

    const response = await apiFetch<{ status: string; data: PmTask[] }>(`${baseURL}/features/pm-calendar/tasks?${params}`)
    return response?.data ?? []
  }

  const fetchTask = async (taskId: string): Promise<PmTask> => {
    const res = await apiFetch<{ status: string; data: PmTask }>(
      `${baseURL}/features/pm-calendar/tasks/${taskId}`
    )
    return res.data
  }

  const fetchPlanActivities = async (planId: string): Promise<{ data: PlanActivity[]; plan_name?: string }> => {
    const res = await apiFetch<{ status: string; data: PlanActivity[]; plan_name?: string }>(
      `${baseURL}/features/pm-calendar/plan/${planId}/activities`
    )
    return { data: res.data || [], plan_name: res.plan_name }
  }

  const validateAssetDates = async (): Promise<{ status: string; data: { issues: any[] }; message: string }> => {
    const res = await apiFetch<{ status: string; data: { issues: any[] }; message: string }>(
      `${baseURL}/features/pm-calendar/validate-asset-properties`
    )
    return res
  }

  return {
    fetchTasks,
    fetchTask,
    fetchPlanActivities,
    validateAssetDates,
  }
}
