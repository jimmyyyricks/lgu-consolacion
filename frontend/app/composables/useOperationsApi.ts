import { useApiFetch } from './useApiFetch'

export interface DashboardStatusCount {
  status: string
  count: number
}

export interface WorkOrderActivityRow {
  id?: string
  workflow_state?: string | null
  description?: string | null
  work_item_type?: string | null
  work_item?: string | null
  start_date?: string | null
  end_date?: string | null
}

export interface WorkOrderRow {
  id?: string
  workflow_state?: string | null
  description?: string | null
  work_order_type?: string | null
  due_date?: string | null
  priority?: string | null
  site?: string | null
  department?: string | null
  activities: WorkOrderActivityRow[]
  activity_count: number
}

export interface PurchaseRequestRow {
  id?: string
  workflow_state?: string | null
  pr_description?: string | null
  date_requested?: string | null
  due_date?: string | null
  requestor?: string | null
  site?: string | null
  department?: string | null
}

export interface InventoryLocationBreakdown {
  inventory_id?: string
  site?: string | null
  location?: string | null
  location_name?: string | null
  store_location?: string | null
  store_name?: string | null
  actual_inv: number
  available_inv: number
  reserved_inv: number
}

export interface InventoryCountRow {
  item_id: string
  item_name: string
  total_actual_inv: number
  total_available_inv: number
  total_reserved_inv: number
  locations: InventoryLocationBreakdown[]
}

export interface OperationalDashboardResponse {
  work_orders: {
    rows: WorkOrderRow[]
    status_counts: DashboardStatusCount[]
    fields: string[]
    activity_fields: string[]
  }
  purchase_requests: {
    rows: PurchaseRequestRow[]
    status_counts: DashboardStatusCount[]
    fields: string[]
  }
  inventory: {
    rows: InventoryCountRow[]
    fields: string[]
    item_fields: string[]
    location_fields: string[]
  }
}

export const useOperationsApi = () => {
  const { apiFetch, baseURL } = useApiFetch()

  return {
    async getOperationalDashboard(params?: {
      workOrderStatus?: string
      purchaseRequestStatus?: string
    }) {
      const query = new URLSearchParams()
      if (params?.workOrderStatus) query.append('work_order_status', params.workOrderStatus)
      if (params?.purchaseRequestStatus) query.append('purchase_request_status', params.purchaseRequestStatus)
      return apiFetch<{ status: string; data: OperationalDashboardResponse }>(
        `${baseURL}/operations/dashboard${query.size ? `?${query.toString()}` : ''}`
      )
    },

    async getWorkOrderTracker(status?: string) {
      const query = new URLSearchParams()
      if (status) query.append('status', status)
      return apiFetch<{ status: string; data: OperationalDashboardResponse['work_orders'] }>(
        `${baseURL}/operations/dashboard/work-orders${query.size ? `?${query.toString()}` : ''}`
      )
    },

    async getPurchaseRequestTracker(status?: string) {
      const query = new URLSearchParams()
      if (status) query.append('status', status)
      return apiFetch<{ status: string; data: OperationalDashboardResponse['purchase_requests'] }>(
        `${baseURL}/operations/dashboard/purchase-requests${query.size ? `?${query.toString()}` : ''}`
      )
    },

    async getInventoryCount() {
      return apiFetch<{ status: string; data: OperationalDashboardResponse['inventory'] }>(
        `${baseURL}/operations/dashboard/inventory`
      )
    },
  }
}
