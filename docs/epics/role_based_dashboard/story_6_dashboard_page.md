# Story 6: Dashboard Page Integration

**Status:** To Do
**Epic:** Metadata-Driven Role-Based Dashboard
**Priority:** P2 — Requires Stories 4 and 5

## Story

As a frontend developer, I need `dashboard.vue` to render all widgets using `<DashboardWidget>` so the page is completely agnostic to widget types and only orchestrates data loading and navigation.

## Context

After Stories 4–5, the composable serves canonical widget metadata and `DashboardWidget.vue` handles all rendering. The page only needs to iterate `selectedDashboard.widgets` and pass each widget to the renderer. All inline widget templates and widget-specific `v-if` blocks currently in the page must be removed.

## Acceptance Criteria

- [ ] All inline widget rendering removed from `dashboard.vue` template
- [ ] Widget iteration: `<DashboardWidget v-for="widget in selectedDashboard.widgets" :key="widget.widget_id" :widget="widget" />`
- [ ] `UPageGrid` (or equivalent grid wrapper) wraps the widget list
- [ ] Loading state: `USkeleton` shown while `isLoading` is true
- [ ] Error state: `UAlert` shown when `error` is not null
- [ ] Empty state: `UPageCard` shown when `selectedDashboard.widgets` is empty
- [ ] `UDashboardNavbar` title is `selectedDashboard.label`
- [ ] `UDashboardToolbar #left` still shows `UNavigationMenu` with `allowedDashboards` selector
- [ ] `isLoading`, `error`, and `selectedDashboard` all come from `useDashboard()` composable
- [ ] No widget-specific imports or type references remain in `dashboard.vue`
- [ ] `pnpm typecheck` passes

## Technical Notes

Page body skeleton (simplified):
```vue
<template>
  <UDashboardPanel id="dashboard" :ui="{ body: 'lg:py-8' }">
    <UDashboardNavbar :title="selectedDashboard?.label" ...>
      <template #leading><UDashboardSidebarCollapse /></template>
    </UDashboardNavbar>
    <UDashboardToolbar>
      <template #left>
        <UNavigationMenu :items="navigationLinks" highlight color="neutral" class="-mx-1 flex-1" />
      </template>
      <template #right>
        <UButton label="Refresh" @click="refresh" />
        <UButton label="Export" />
      </template>
    </UDashboardToolbar>

    <template #body>
      <div class="flex flex-col gap-6 w-full">
        <template v-if="isLoading">
          <USkeleton class="h-32 w-full" v-for="n in 3" :key="n" />
        </template>
        <template v-else-if="error">
          <UAlert color="red" :description="error" />
        </template>
        <template v-else-if="!selectedDashboard?.widgets?.length">
          <UPageCard title="No widgets available" />
        </template>
        <template v-else>
          <UPageGrid>
            <DashboardWidget
              v-for="widget in selectedDashboard.widgets"
              :key="widget.widget_id"
              :widget="widget"
            />
          </UPageGrid>
        </template>
      </div>
    </template>
  </UDashboardPanel>
</template>
```

## Tasks

1. Remove all inline widget templates and widget-specific script logic from `dashboard.vue`
2. Replace with `<DashboardWidget>` loop inside `<UPageGrid>`
3. Wire `isLoading`, `error`, `selectedDashboard`, `allowedDashboards` from `useDashboard()`
4. Ensure `navigationLinks` computed still uses `allowedDashboards` from composable
5. Run `pnpm typecheck`

## Definition of Done

- [ ] No widget-specific code in `dashboard.vue`
- [ ] `DashboardWidget` loop renders all widgets
- [ ] Loading, error, and empty states all work
- [ ] `pnpm typecheck` passes
