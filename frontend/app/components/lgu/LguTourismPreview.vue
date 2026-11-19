<script setup lang="ts">
const { data, error } = await usePublicContent({
  kind: 'tourism',
  limit: 3
})
</script>

<template>
  <div
    id="tourism-preview"
    class="min-w-0"
  >
    <UCard
      variant="outline"
      :ui="{ root: 'h-full overflow-hidden', body: 'p-0!' }"
    >
      <div>
        <div class="relative h-40 bg-muted sm:h-48">
          <img
            src="/images/consolacion-cover-photo.jpg"
            alt="Consolacion Municipal Hall and community artwork"
            class="absolute inset-0 size-full object-cover object-left"
            loading="lazy"
          >
        </div>
        <div class="bg-success-50/60 p-5 sm:p-7">
          <ul
            v-if="data.length"
            class="divide-y divide-default"
          >
            <li
              v-for="item in data.slice(0, 2)"
              :key="item.id"
            >
              <NuxtLink
                :to="publicContentPath(item)"
                class="group flex min-h-14 items-center justify-between gap-3 py-2"
              >
                <span>
                  <span class="block font-medium text-highlighted group-hover:text-primary">
                    {{ item.title }}
                  </span>
                </span>
                <UIcon
                  name="i-lucide-arrow-right"
                  class="size-5 shrink-0 text-success-700"
                />
              </NuxtLink>
            </li>
          </ul>

          <p
            v-else-if="error"
            class="mt-5 leading-7 text-muted"
          >
            Tourism information is temporarily unavailable.
          </p>
          <p
            v-else
            class="mt-5 leading-7 text-muted"
          >
            Visitor information will be published here.
          </p>

          <UButton
            to="/tourism"
            variant="link"
            size="lg"
            trailing-icon="i-lucide-arrow-right"
            class="mt-4 px-0 text-primary-700 dark:text-primary-300"
          >
            Explore Tourism
          </UButton>
        </div>
      </div>
    </UCard>
  </div>
</template>
