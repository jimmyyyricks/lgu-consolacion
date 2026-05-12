<template>
  <div
    class="pm-calendar-page h-full min-h-0 flex flex-col gap-3 overflow-hidden p-6"
  >
    <!-- Toolbar -->
    <div class="flex-1 min-h-0 flex flex-col overflow-hidden">
      <!-- Toolbar -->
      <div
        class="shrink-0 flex items-center justify-between bg-card p-4 border border-muted dark:border-gray-800 rounded-t-lg"
      >
        <div class="flex items-center gap-2">
          <!-- View switcher (left) -->
          <UFieldGroup size="md">
            <UButton
              v-for="view in views"
              :key="view.value"
              :label="view.label"
              :variant="activeView === view.value ? 'solid' : 'outline'"
              :color="activeView === view.value ? 'primary' : 'neutral'"
              @click="setActiveView(view.value)"
            />
          </UFieldGroup>

          <!-- ALERT BUTTON -->
          <UButton
            v-if="issues.length > 0"
            icon="i-lucide-alert-triangle"
            color="error"
            variant="solid"
            size="md"
            @click="configurationModalOpen = true"
          >
            {{ issues.length }}
          </UButton>
        </div>
        <!-- Header label (center) -->
        <h3 class="text-base font-semibold min-w-[160px] text-center">
          {{ headerLabel }}
        </h3>

        <!-- Right: navigation -->
        <div class="flex items-center gap-2">
          <UButton
            icon="i-lucide-chevron-left"
            variant="outline"
            size="md"
            @click="onPrev"
            color="neutral"
          />
          <UButton
            label="Today"
            variant="outline"
            size="md"
            color="neutral"
            @click="goToToday"
          />
          <UButton
            icon="i-lucide-chevron-right"
            variant="outline"
            size="md"
            @click="onNext"
            color="neutral"
          />
        </div>
      </div>

      <!-- Loading -->
      <div
        v-if="loading"
        class="flex-1 min-h-0 flex items-center justify-center border border-muted"
      >
        <UIcon
          name="i-lucide-loader-2"
          class="w-6 h-6 animate-spin text-gray-400"
        />
      </div>

      <!-- ── Views ──────────────────────────────────────────────────────────── -->
      <CalendarMonthView
        v-else-if="activeView === 'month'"
        ref="activeCalendarRef"
        v-model="calendarValue"
        :tasks-by-date="tasksByDate"
        @click-day="onClickDay"
        @click-date="onClickDate"
        @open-detail="openDetail"
        @show-all-tasks="showAllTasks"
      />

      <CalendarDayView
        v-else-if="activeView === 'day'"
        ref="activeCalendarRef"
        v-model="calendarValue"
        :tasks-by-date="tasksByDate"
        @click-interval="onClickInterval"
        @open-detail="openDetail"
      />

      <CalendarWeekView
        v-else-if="activeView === 'week'"
        ref="activeCalendarRef"
        v-model="calendarValue"
        :tasks-by-date="tasksByDate"
        @click-interval="onClickInterval"
        @open-detail="openDetail"
      />
    </div>

    <!-- Detail Modal -->
    <UModal
      v-model:open="detailModalOpen"
      :title="truncateTitle(selectedTask?.activity_name || 'Task Details', 50)"
      :description="selectedTask?.id"
      :ui="{ content: 'max-w-4xl' }"
    >
      <template #body>
        <div class="space-y-4" v-if="selectedTask">
          <!-- PM Indicator -->
          <div v-if="selectedTask.plan_id" class="flex items-center gap-2">
            <UBadge color="primary" variant="subtle" size="sm">
              <UIcon name="i-lucide-calendar-clock" class="w-3 h-3 mr-1" />
              Planned Maintenance
            </UBadge>
            <span class="text-xs text-gray-500"
              >No Maintenance Request created yet</span
            >
          </div>

          <!-- Status Badge -->
          <div class="flex items-center justify-between">
            <UBadge
              :color="getWorkflowStateColor(selectedTask.workflow_state)"
              variant="solid"
              size="lg"
            >
              {{ selectedTask.workflow_state }}
            </UBadge>
          </div>

          <!-- Details Card -->
          <UCard variant="outline">
            <template #header>
              <h4 class="text-sm font-semibold">Task Details</h4>
            </template>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span class="text-gray-500 text-xs">Date</span>
                <p class="font-medium">{{ selectedTask.due_date }}</p>
              </div>
              <div>
                <span class="text-gray-500 text-xs">Time</span>
                <p class="font-medium">{{ selectedTask.start_time }}</p>
              </div>
              <div>
                <span class="text-gray-500 text-xs">Assigned To</span>
                <p class="font-medium">
                  {{
                    selectedTask.assigned_to_name || selectedTask.laborer || "—"
                  }}
                </p>
              </div>
              <div>
                <span class="text-gray-500 text-xs">Site</span>
                <p class="font-medium">
                  {{ selectedTask.site_name || selectedTask.site || "—" }}
                </p>
              </div>
              <div
                v-if="selectedTask.department_name || selectedTask.department"
              >
                <span class="text-gray-500 text-xs">Department</span>
                <p class="font-medium">
                  {{
                    selectedTask.department_name ||
                    selectedTask.department ||
                    "—"
                  }}
                </p>
              </div>
            </div>
          </UCard>

          <!-- Notes -->
          <div v-if="selectedTask.notes" class="text-sm">
            <span class="text-gray-500 text-xs">Notes</span>
            <p class="mt-1">{{ selectedTask.notes }}</p>
          </div>
        </div>
      </template>
    </UModal>

    <!-- Plan Activities Modal -->
    <UModal
      v-model:open="planActivitiesModalOpen"
      :title="'Planned Maintenance Activities'"
      :description="`Maint Plan: ${selectedPlanName || selectedPlanId}`"
      :ui="{ content: 'max-w-2xl' }"
    >
      <template #body>
        <div v-if="selectedPlanActivities.length > 0" class="space-y-3">
          <UPageCard
            v-for="(activity, index) in selectedPlanActivities"
            :key="index"
            :title="activity.activity_name"
            :icon="getSchedulingTypeIcon(activity.scheduling_type)"
            variant="outline"
            class="w-full"
            orientation="horizontal"
          >
            <div class="space-y-2">
              <div class="flex justify-end">
                <UBadge
                  :color="getSchedulingTypeColor(activity.scheduling_type)"
                  variant="subtle"
                  size="md"
                >
                  {{
                    activity.scheduling_type.charAt(0).toUpperCase() +
                    activity.scheduling_type.slice(1)
                  }}
                </UBadge>
              </div>
              <div class="flex justify-end items-end text-right">
                <div v-if="activity.frequency">
                  <!-- label -->
                  <span class="text-gray-400 text-xs uppercase">Frequency</span>
                  <!-- value -->
                  <p class="text-md font-bold text-gray-700">
                    {{ activity.frequency }}
                  </p>
                </div>
                <div v-if="activity.interval">
                  <!-- label -->
                  <span class="text-gray-400 text-xs uppercase">Interval</span>
                  <!-- value -->
                  <p class="font-bold text-gray-700 text-md">
                    {{ activity.interval }}
                    <span
                      v-if="activity.interval_unit_of_measure_name"
                      class="text-md font-bold"
                    >
                      {{ activity.interval_unit_of_measure_name }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
            <template #footer v-if="selectedTask">
              <div class="flex items-center gap-2">
                <UButton
                  v-if="selectedTask.asset_id"
                  :label="`View Asset ${selectedTask.asset_display_name || selectedTask.asset_id}`"
                  :to="`/asset/${selectedTask.asset_id}`"
                  trailing-icon="i-lucide-arrow-right"
                  color="neutral"
                  variant="subtle"
                  size="md"
                />
                <span v-else class="font-medium text-gray-700">
                  {{ selectedTask.asset_display_name || "—" }}
                </span>
              </div>
            </template>
          </UPageCard>
        </div>
        <div v-else class="text-center text-gray-500 py-4">
          No planned maintenance activities found for this plan.
        </div>
      </template>
    </UModal>

    <!-- Day Tasks Modal -->
    <UModal
      v-model:open="dayTasksModalOpen"
      :title="`Tasks for ${selectedDate}`"
      :description="`${selectedDayTasks.length} tasks scheduled`"
      :ui="{ content: 'max-w-3xl' }"
    >
      <template #body>
        <div v-if="selectedDayTasks.length > 0" class="space-y-3">
          <UPageCard
            v-for="task in selectedDayTasks"
            :key="task.id"
            :title="task.activity_name"
            variant="outline"
            class="w-full"
            orientation="horizontal"
          >
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <UBadge
                  :color="getWorkflowStateColor(task.asset_workflow_state)"
                  variant="subtle"
                  size="md"
                >
                  {{ task.asset_workflow_state }}
                </UBadge>
                <span class="text-xs text-gray-500">{{
                  task.asset_display_name || task.asset_id
                }}</span>
              </div>
              <div class="flex justify-end items-center gap-4 text-sm">
                <div>
                  <span class="text-gray-400 text-xs uppercase">Time</span>
                  <p class="font-medium">{{ task.start_time }}</p>
                </div>
                <div>
                  <span class="text-gray-400 text-xs uppercase">Due</span>
                  <p class="font-medium">{{ task.due_date }}</p>
                </div>
              </div>
              <div class="flex justify-end">
                <UButton
                  label="View Details"
                  size="sm"
                  color="neutral"
                  variant="outline"
                  @click="openDetail(task)"
                />
              </div>
            </div>
          </UPageCard>
        </div>
        <div v-else class="text-center text-gray-500 py-4">
          No tasks scheduled for this day.
        </div>
      </template>
    </UModal>

    <!-- Configuration Issues Modal -->
    <UModal
      v-model:open="configurationModalOpen"
      title="PM Issues"
      description="Configuration and asset property issues"
      :ui="{ content: 'max-w-3xl' }"
    >
      <template #body>
        <div v-if="issues.length > 0">
          <UAlert
            color="error"
            variant="solid"
            :title="`${issues.length} Issues Found`"
            description="Property references must be configured on maintenance calendars and intervals, and assets must have required property values set."
          />

          <!-- Plan Issues -->
          <div v-if="planIssues.length > 0" class="mt-4">
            <h4 class="text-sm font-semibold mb-2">Plan Issues</h4>
            <UAlert
              v-for="(issue, index) in planIssues"
              :key="`plan-${index}`"
              :title="issue.maintenance_plan_name"
              :icon="
                issue.type === 'calendar'
                  ? 'i-lucide-calendar'
                  : 'i-lucide-clock'
              "
              :description="issue.issue"
              color="neutral"
              variant="subtle"
              orientation="horizontal"
              class="my-4"
              :actions="[
                {
                  label: 'View Plan',
                  trailingIcon: 'i-lucide-arrow-right',
                  size: 'md',
                  color: 'neutral',
                  variant: 'solid',
                  onClick: () => {
                    void navigateTo(
                      `/maintenance_plan/${issue.maintenance_plan_id}`,
                    );
                  },
                },
              ]"
            />
          </div>

          <!-- Asset Issues -->
          <div v-if="assetIssues.length > 0" class="mt-4">
            <h4 class="text-sm font-semibold mb-2">Asset Issues</h4>
            <UAlert
              v-for="(issue, index) in assetIssues"
              :key="`asset-${index}`"
              :title="issue.asset_display_name"
              :icon="'i-lucide-alert-triangle'"
              :description="issue.issue"
              color="warning"
              variant="subtle"
              orientation="horizontal"
              class="my-4"
              :actions="[
                {
                  label: 'View Asset',
                  trailingIcon: 'i-lucide-arrow-right',
                  size: 'md',
                  color: 'neutral',
                  variant: 'solid',
                  onClick: () => {
                    void navigateTo(`/asset/${issue.asset_id}`);
                  },
                },
              ]"
            />
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import type { PmTask, PlanActivity } from "~/composables/usePmCalendar";
import "~/components/calendar/qcalendar-theme.css";

const toast = useToast();
const { fetchTask, fetchPlanActivities, validateAssetDates } = usePmCalendar();
const calendarCache = useCalendarCache();

// ── View switcher ────────────────────────────────────────────────────────────
const views = [
  { value: "day", label: "Day" },
  { value: "week", label: "Week" },
  { value: "month", label: "Month" },
] as const;
const activeView = ref<"month" | "week" | "day">("month");

// ── State ────────────────────────────────────────────────────────────────────
const loading = ref(true);

const currentYear = ref(new Date().getFullYear());
const currentMonth = ref(new Date().getMonth() + 1);

const tasks = ref<PmTask[]>([]);

const detailModalOpen = ref(false);
const selectedTask = ref<PmTask | null>(null);
const planActivitiesModalOpen = ref(false);
const selectedPlanActivities = ref<PlanActivity[]>([]);
const selectedPlanId = ref<string | null>(null);
const selectedPlanName = ref<string | null>(null);

const issues = ref<any[]>([]);
const configurationModalOpen = ref(false);

const dayTasksModalOpen = ref(false);
const selectedDayTasks = ref<PmTask[]>([]);
const selectedDate = ref<string>("");

const calendarValue = ref("");

// Computed properties to separate issues by type
const planIssues = computed(() =>
  issues.value.filter((i) => i.issue_type === "configuration"),
);
const assetIssues = computed(() =>
  issues.value.filter((i) => i.issue_type === "asset"),
);

// ── Active calendar ref (exposed by each view component) ─────────────────────
const activeCalendarRef = ref<{
  prev: () => void;
  next: () => void;
  moveToToday: () => void;
} | null>(null);

function parseYmd(value: string) {
  const [y, m, d] = value.split("-").map((x) => Number(x));
  return new Date(y || 1970, (m || 1) - 1, d || 1);
}

function formatLongDate(d: Date) {
  return d.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function startOfWeek(d: Date) {
  const day = d.getDay();
  const diff = (day + 6) % 7;
  const out = new Date(d);
  out.setDate(d.getDate() - diff);
  out.setHours(0, 0, 0, 0);
  return out;
}

function endOfWeek(d: Date) {
  const s = startOfWeek(d);
  const out = new Date(s);
  out.setDate(s.getDate() + 6);
  return out;
}

const headerLabel = computed(() => {
  if (activeView.value === "month") return monthLabel.value;
  if (!calendarValue.value) return monthLabel.value;

  const d = parseYmd(calendarValue.value);
  if (activeView.value === "day") {
    return formatLongDate(d);
  }

  // week
  const s = startOfWeek(d);
  const e = endOfWeek(d);
  const sameMonth =
    s.getMonth() === e.getMonth() && s.getFullYear() === e.getFullYear();
  const sLabel = s.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
  const eLabel = e.toLocaleDateString("en-US", {
    month: sameMonth ? undefined : "short",
    day: "numeric",
    year: "numeric",
  });
  return `${sLabel} – ${eLabel}`;
});

// ── Computed ─────────────────────────────────────────────────────────────────
const monthLabel = computed(() => {
  const d = new Date(currentYear.value, currentMonth.value - 1, 1);
  return d.toLocaleDateString("en-US", { month: "long", year: "numeric" });
});

const tasksByDate = computed(() => {
  const m = new Map<string, PmTask[]>();
  tasks.value.forEach((t) => {
    if (!m.has(t.due_date)) m.set(t.due_date, []);
    m.get(t.due_date)!.push(t);
  });
  m.forEach((arr) =>
    arr.sort((a, b) => (a.start_time || "").localeCompare(b.start_time || "")),
  );
  return m;
});

// ── View Data Loading ─────────────────────────────────────────────────────────
async function loadViewData(
  view: "month" | "week" | "day",
  year: number,
  month: number,
) {
  loading.value = true;
  try {
    // Load tasks only (holidays not needed for read-only views)
    tasks.value = await calendarCache.getOrFetchTasks(year, month);
  } catch (e: any) {
    toast.add({
      title: "Error loading calendar data",
      description: e?.message || "Unknown error",
      color: "error",
    });
  } finally {
    loading.value = false;
  }
}

function setActiveView(view: "month" | "week" | "day") {
  activeView.value = view;
  // Reload data when switching views
  loadViewData(view, currentYear.value, currentMonth.value);
}

function getWorkflowStateColor(
  state: string,
): "primary" | "neutral" | "success" | "warning" | "error" {
  const colorMap: Record<
    string,
    "primary" | "neutral" | "success" | "warning" | "error"
  > = {
    Draft: "neutral",
    "Pending Approval": "warning",
    Approved: "primary",
    Release: "primary",
    Completed: "success",
    Scheduled: "primary",
    Active: "success",
    "Under Maintenance": "warning",
    Acquired: "neutral",
  };
  return colorMap[state] || "neutral";
}

function getSchedulingTypeColor(
  type: string,
): "primary" | "neutral" | "success" {
  const colorMap: Record<string, "primary" | "neutral" | "success"> = {
    calendar: "primary",
    interval: "success",
    none: "neutral",
  };
  return colorMap[type] || "neutral";
}

function truncateTitle(title: string, maxLength: number): string {
  if (!title) return "";
  return title.length > maxLength ? title.slice(0, maxLength) + "..." : title;
}

function getSchedulingTypeIcon(type: string): string {
  const iconMap: Record<string, string> = {
    calendar: "i-lucide-calendar",
    interval: "i-lucide-clock",
    none: "i-lucide-minus",
  };
  return iconMap[type] || "i-lucide-circle";
}

// ── Helpers ──────────────────────────────────────────────────────────────────
function formatDate(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

// ── Navigation ───────────────────────────────────────────────────────────────
function goToToday() {
  activeCalendarRef.value?.moveToToday();
}

function onPrev() {
  activeCalendarRef.value?.prev();
}

function onNext() {
  activeCalendarRef.value?.next();
}

watch(
  () => calendarValue.value,
  async (val, oldVal) => {
    const m = parseYmd(val);
    currentYear.value = m.getFullYear();
    currentMonth.value = Number(m.getMonth() + 1);
    const oldMonth = oldVal ? oldVal.slice(0, 7) : "";
    if (val.slice(0, 7) !== oldMonth) {
      loadViewData(activeView.value, currentYear.value, currentMonth.value);
    }
  },
  { immediate: true },
);

async function openDetail(task: PmTask) {
  try {
    // If task has plan_id, it's a Maintenance Plan - fetch its activities
    if (task.plan_id) {
      selectedTask.value = task;
      const response = await fetchPlanActivities(task.plan_id);
      // Filter to show only the specific activity that matches this calendar task
      selectedPlanActivities.value = task.planned_maintenance_activity
        ? response.data.filter(
            (activity: any) =>
              activity.id === task.planned_maintenance_activity ||
              activity.planned_maintenance_activity ===
                task.planned_maintenance_activity,
          )
        : response.data;
      selectedPlanId.value = task.plan_id;
      selectedPlanName.value = response.plan_name || task.plan_id;
      planActivitiesModalOpen.value = true;
    } else {
      const fullTask = await fetchTask(task.id);
      selectedTask.value = fullTask;
      detailModalOpen.value = true;
    }
  } catch (e: any) {
    // Error loading task details
    toast.add({
      title: "Error",
      description: "Failed to load task details",
      color: "error",
    });
  }
}

// ── QCalendar handlers ───────────────────────────────────────────────────────
function onClickInterval(_payload: any) {
  notifyReadOnly();
}

function onClickDay(_payload: any) {
  notifyReadOnly();
}

function onClickDate(_payload: any) {
  notifyReadOnly();
}

function notifyReadOnly() {
  toast.add({
    title: "Read-only",
    description:
      "Create and updates must be done through the standard process, not in the calendar view.",
    color: "neutral",
  });
}

function showAllTasks(date: string) {
  selectedDate.value = date;
  selectedDayTasks.value = tasksByDate.value.get(date) || [];
  dayTasksModalOpen.value = true;
}

// ── Init ─────────────────────────────────────────────────────────────────────
onMounted(async () => {
  const today = new Date();
  calendarValue.value = formatDate(today);

  // Load validation results
  try {
    const response = await validateAssetDates();
    if (response.status === "success") {
      const data = response.data as any;
      if (data && data.issues) {
        issues.value = data.issues || [];
      }
    }
  } catch (e: any) {
    console.error("Failed to validate asset dates:", e);
  }
});
</script>
