<script setup lang="ts">
const { data, error, pending } = await usePublicContent({
  kind: "government_action",
  limit: 3,
});
</script>

<template>
  <UCard variant="outline" :ui="{ root: 'h-full', body: 'p-5 sm:p-6' }">
    <template #title>
      <h3
        id="other-updates-heading"
        class="font-domine text-xl font-semibold leading-snug text-highlighted"
      >
        Other Updates
      </h3>
    </template>
    <aside aria-labelledby="other-updates-heading">
      <UAlert
        v-if="error"
        class="mt-5"
        color="error"
        variant="subtle"
        title="Updates Are Temporarily Unavailable"
      />
      <div
        v-else-if="pending"
        class="mt-4 space-y-3"
        aria-label="Loading Quick Updates"
      >
        <USkeleton v-for="item in 3" :key="item" class="h-20 w-full" />
      </div>
      <div v-else-if="data.length" class="grid gap-3">
        <UPageCard
          v-for="item in data"
          :key="item.id"
          :to="publicContentPath(item)"
          :title="item.title"
          :description="publicContentDate(item.record_date) || undefined"
          orientation="vertical"
          variant="outline"
          :ui="{
            root: 'min-w-0',
            container: 'w-full min-w-0 gap-3',
            wrapper: 'w-full min-w-0',
            title: 'line-clamp-2 w-full text-sm font-semibold leading-snug',
            description: 'mt-1 w-full text-sm',
          }"
        />
      </div>
      <UAlert
        v-else
        class="mt-5"
        color="neutral"
        variant="subtle"
        title="No Quick Updates Yet"
      />
      <UButton
        to="/about/actions"
        variant="link"
        size="lg"
        trailing-icon="i-lucide-arrow-right"
        class="mt-2 px-0"
      >
        All Government Updates
      </UButton>
    </aside>
  </UCard>
</template>
