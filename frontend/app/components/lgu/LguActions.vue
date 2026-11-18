<script setup lang="ts">
const { data, error, pending } = await usePublicContent({
  kind: 'government_action',
  limit: 3
})
</script>

<template>
  <UCard
    variant="outline"
    :ui="{ root: 'h-full', body: 'p-5 sm:p-6' }"
  >
    <template #title>
      <h3
        id="quick-updates-heading"
        class="font-domine text-xl font-semibold leading-snug text-highlighted"
      >
        Government and planning updates
      </h3>
    </template>
    <aside aria-labelledby="quick-updates-heading">
      <UAlert
        v-if="error"
        class="mt-5"
        color="error"
        variant="subtle"
        title="Updates are temporarily unavailable"
      />
      <div
        v-else-if="pending"
        class="mt-4 space-y-3"
        aria-label="Loading quick updates"
      >
        <USkeleton
          v-for="item in 3"
          :key="item"
          class="h-12 w-full"
        />
      </div>
      <ul
        v-else-if="data.length"
        class="mt-3 divide-y divide-default"
      >
        <li
          v-for="item in data"
          :key="item.id"
          class="py-3 first:pt-0 last:pb-0"
        >
          <NuxtLink
            :to="publicContentPath(item)"
            class="group flex min-h-11 items-start gap-3 py-1"
          >
            <UIcon
              name="i-lucide-bell"
              class="mt-1 size-4 shrink-0 text-primary"
            />
            <span>
              <span class="block font-medium leading-6 text-highlighted group-hover:text-primary">
                {{ item.title }}
              </span>
              <span class="mt-1 block text-muted">
                {{ publicContentDate(item.record_date) }}
              </span>
            </span>
          </NuxtLink>
        </li>
      </ul>
      <UAlert
        v-else
        class="mt-5"
        color="neutral"
        variant="subtle"
        title="No quick updates yet"
      />
      <UButton
        to="/about/actions"
        variant="link"
        size="lg"
        trailing-icon="i-lucide-arrow-right"
        class="mt-2 px-0"
      >
        All government updates
      </UButton>
    </aside>
  </UCard>
</template>
