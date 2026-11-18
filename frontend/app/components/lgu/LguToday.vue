<template>
  <UPageSection
    id="today"
    title="Weather and reminders"
    description="Weather, public updates and practical reminders in one place."
    aria-label="Weather and reminders"
    class="bg-primary-50 dark:bg-primary-950/40"
    :ui="{
      container: 'gap-7 py-12 sm:gap-8 sm:py-14 lg:py-16',
      title: 'text-left font-domine text-3xl font-semibold leading-tight tracking-normal sm:text-4xl lg:text-4xl',
      description: 'mt-3 text-left text-base leading-7 text-toned sm:text-base'
    }"
  >
    <div class="grid gap-8 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)] lg:gap-10">
      <UCard
        variant="outline"
        :ui="{ root: 'bg-elevated/60', body: 'p-5 sm:p-6' }"
      >
        <template #title>
          <h3 class="font-domine text-xl font-semibold leading-snug text-highlighted">
            Weather
          </h3>
        </template>
        <div class="flex items-center gap-4">
          <UIcon
            name="i-lucide-cloud-sun"
            class="size-10 shrink-0 text-primary"
          />
          <p class="leading-7 text-toned">
            Live weather updates are not available on this site yet.
          </p>
        </div>
        <p class="mt-4 border-t border-default pt-4 leading-6 text-muted">
          Check a current local forecast before traveling.
        </p>
      </UCard>

      <LguActions />
    </div>
  </UPageSection>
</template>
