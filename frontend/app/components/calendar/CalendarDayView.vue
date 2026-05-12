<template>
  <div class="flex-1 min-h-0 overflow-auto qcal-wrap border border-muted">
    <component
      :is="QCalendarDayComp"
      date-header="inline"
      ref="calendarRef"
      v-model="model"
      no-scroll
      view="day"
      :interval-start="8"
      :interval-count="30"
      :interval-minutes="30"
      hoverable
      focusable
      @click-interval="$emit('click-interval', $event)"
    >
      <template #day-body="{ scope }">
        <template
          v-for="task in tasksByDate.get(scope.timestamp.date) || []"
          :key="task.id"
        >
          <div
            class="calendar-task-item calendar-task-item--absolute"
            :style="getEventStyle(task)"
            :title="`${task.start_time} ${task.activity_name}`"
            @click.stop="$emit('open-detail', task)"
          >
            <p
              class="font-semibold truncate"
              :style="{ color: task.color, marginLeft: '8px' }"
            >
              {{ task.activity_name }}
            </p>
          </div>
        </template>
      </template>
    </component>
  </div>
</template>

<script setup lang="ts">
import QCalendarDayPlugin from "@quasar/quasar-ui-qcalendar/QCalendarDay";
import type { PmTask } from "~/composables/usePmCalendar";

const QCalendarDayComp = (QCalendarDayPlugin as any).QCalendarDay;

const props = defineProps<{
  tasksByDate: Map<string, PmTask[]>;
}>();

defineEmits<{
  "click-interval": [payload: any];
  "open-detail": [task: PmTask];
}>();

const model = defineModel<string>({ required: true });

const calendarRef = ref<any>(null);

function timeToOffset(timeStr: string | undefined): number {
  if (!timeStr) return 0;
  const [h, m] = timeStr.split(":").map(Number);
  const intervalStart = 8; // Match :interval-start="8"
  const intervalHeight = 40; // QCalendar default interval height
  const intervalMinutes = 30; // Match :interval-minutes="30"

  const totalMinutes = (h! - intervalStart) * 60 + (m || 0);
  return (totalMinutes / intervalMinutes) * intervalHeight;
}

function timeToMinutes(timeStr: string | undefined): number {
  if (!timeStr) return 0;
  const [h, m] = timeStr.split(":").map(Number);
  return (h || 0) * 60 + (m || 0);
}

type PositionedTask = {
  task: PmTask;
  left: number;
  width: number;
  top: number;
  height: number;
};

function layoutEvents(tasks: PmTask[]): PositionedTask[] {
  if (tasks.length === 0) return [];

  const durationMinutes = 30; // Default duration
  const items = tasks
    .slice()
    .sort((a, b) => timeToMinutes(a.start_time) - timeToMinutes(b.start_time))
    .map((task) => ({
      task,
      start: timeToMinutes(task.start_time),
      end: timeToMinutes(task.start_time) + durationMinutes,
    }));

  // Find overlapping groups and assign lanes
  const lanes: Array<{ end: number }> = [];
  const positioned: Array<{ task: PmTask; lane: number }> = [];

  for (const item of items) {
    const laneIndex = lanes.findIndex((lane) => lane.end <= item.start);
    if (laneIndex === -1) {
      lanes.push({ end: item.end });
      positioned.push({ task: item.task, lane: lanes.length - 1 });
    } else {
      lanes[laneIndex]!.end = item.end;
      positioned.push({ task: item.task, lane: laneIndex });
    }
  }

  const maxLanes = Math.max(lanes.length, 1);
  const rowHeight = 40;
  const rowGap = 2;

  return positioned.map(({ task, lane }) => ({
    task,
    left: (lane / maxLanes) * 100,
    width: (1 / maxLanes) * 100,
    top: timeToOffset(task.start_time),
    height: rowHeight,
  }));
}

function getEventStyle(task: PmTask): Record<string, string> {
  // Get all tasks for the current date to calculate layout
  const currentDate = model.value;
  const tasksForDate = props.tasksByDate.get(currentDate) || [];
  const positioned = layoutEvents(tasksForDate);
  const position = positioned.find((p) => p.task.id === task.id);

  return {
    top: `${position?.top || 0}px`,
    height: `${position?.height || 40}px`,
    backgroundColor: (task.color || "#94a3b8") + "22",
    borderLeft: `6px solid ${task.color || "#94a3b8"}`,
    position: "absolute",
    left: position ? `${position.left}%` : "0px",
    width: position ? `${position.width}%` : "100%",
  };
}

function formatTime(hour: number): string {
  const period = hour >= 12 ? "PM" : "AM";
  const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
  return `${displayHour}${period}`;
}

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

.qcal-wrap :deep(.q-calendar-day__head) {
  position: sticky;
  top: 0;
  z-index: 3;
  background: var(--calendar-background);
}

.qcal-wrap :deep(.q-calendar__header--inline) {
  padding: 4px;
}

.qcal-wrap :deep(.q-calendar-day__head--weekday) {
  padding: 4px;
  font-size: 12px;
  text-transform: uppercase;
  font-weight: 400;
}

.qcal-wrap :deep(.q-calendar-day__head--date) {
  padding: 4px;
}
</style>
