<template>
  <div
    ref="wrapRef"
    class="flex-1 min-h-0 overflow-auto qcal-wrap border border-muted"
  >
    <QCalendarMonth
      ref="calendarRef"
      v-model="model"
      :style="calendarStyle"
      :weekdays="[1, 2, 3, 4, 5, 6, 0]"
      hoverable
      focusable
      @click-day="$emit('click-day', $event)"
      @click-date="$emit('click-date', $event)"
    >
      <template #day="{ scope }">
        <div class="space-y-1 px-1">
          <div
            v-for="task in (tasksByDate.get(scope.timestamp.date) || []).slice(
              0,
              2,
            )"
            :key="task.id"
            class="calendar-task-item"
            :style="{
              backgroundColor:
                getAssetStateColor(task.asset_workflow_state) + '22',
              borderLeft: `6px solid ${getAssetStateColor(task.asset_workflow_state)}`,
            }"
            :title="`${task.start_time || ''} ${task.activity_name} (${task.asset_display_name || task.asset_id})`"
            draggable="false"
            @click.stop="$emit('open-detail', task)"
          >
            <span class="text-gray-600 dark:text-gray-300 shrink-0">{{
              task.start_time?.slice(0, 5) || ""
            }}</span>
            <span
              class="truncate"
              :style="{ color: getAssetStateColor(task.asset_workflow_state) }"
              >{{ task.activity_name }}</span
            >
          </div>
          <div
            v-if="(tasksByDate.get(scope.timestamp.date) || []).length > 2"
            class="calendar-task-item text-xs text-gray-500 cursor-pointer hover:text-gray-700"
            @click.stop="$emit('show-all-tasks', scope.timestamp.date)"
          >
            and
            {{ (tasksByDate.get(scope.timestamp.date) || []).length - 2 }} more
          </div>
        </div>
      </template>
    </QCalendarMonth>
  </div>
</template>

<script setup lang="ts">
import { QCalendarMonth, today } from "@quasar/quasar-ui-qcalendar";
import type { Timestamp } from "@quasar/quasar-ui-qcalendar";
import "@quasar/quasar-ui-qcalendar/index.css";
import { useResizeObserver } from "@vueuse/core";
import type { PmTask } from "~/composables/usePmCalendar";

const props = defineProps<{
  tasksByDate: Map<string, PmTask[]>;
}>();

defineEmits<{
  "click-day": [payload: any];
  "click-date": [payload: any];
  "open-detail": [task: PmTask];
  "show-all-tasks": [date: string];
}>();

function getAssetStateColor(state: string): string {
  const colorMap: Record<string, string> = {
    Active: "#22c55e",
    "Under Maintenance": "#f59e0b",
    Acquired: "#6b7280",
    Unknown: "#3b82f6",
  };
  return colorMap[state] || "#3b82f6";
}

const model = defineModel<string>({ required: true });

const calendarRef = ref<QCalendarMonth>();
const wrapRef = ref<HTMLElement | null>(null);
const wrapHeight = ref(0);

useResizeObserver(wrapRef, (entries) => {
  const entry = entries[0];
  if (!entry) return;
  wrapHeight.value = Math.round(entry.contentRect.height);
});

const dayHeight = computed(() => {
  const h = wrapHeight.value;
  if (!h) return 50;
  const headerAndGutters = 56;
  const rows = 6;
  const v = Math.floor((h - headerAndGutters) / rows);
  return Math.max(50, Math.min(220, v));
});

const calendarStyle = computed(() => {
  return {
    display: "flex",
    width: "100%",
    height: "100%",
  };
});

defineExpose({
  prev: () => calendarRef.value?.prev(),
  next: () => calendarRef.value?.next(),
  moveToToday: () => calendarRef.value?.moveToToday(),
});
</script>

<style scoped>
.qcal-wrap :deep(.q-calendar) {
  overflow: unset !important;
}

.qcal-wrap :deep(.q-calendar-month__head) {
  position: sticky !important;
  top: 0;
  z-index: 3;
  background: var(--calendar-background);
}

.qcal-wrap :deep(.q-calendar-month__day--label__wrapper) {
  display: flex;
  margin: 8px 0;
  overflow: visible;
}

.qcal-wrap :deep(.q-calendar-month__day--label) {
  font-size: 12px;
  outline: none;
  overflow: visible;
}

.qcal-wrap :deep(.q-calendar-month__head .q-calendar__ellipsis) {
  text-transform: uppercase;
  font-size: 12px;
  padding: 6px;
}
</style>
