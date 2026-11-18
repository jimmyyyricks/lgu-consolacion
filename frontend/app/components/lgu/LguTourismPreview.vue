<script setup lang="ts">
const { data, error } = await usePublicContent({
  kind: 'tourism',
  limit: 3
})
</script>

<template>
  <UPageSection
    id="tourism-preview"
    title="Tourism in Consolacion"
    description="Local places, community stories and visitor information."
    aria-label="Tourism in Consolacion"
    :ui="{
      container: 'gap-7 py-12 sm:gap-8 sm:py-14 lg:py-16',
      title: 'text-left font-domine text-3xl font-semibold leading-tight tracking-normal sm:text-4xl lg:text-4xl',
      description: 'mt-3 text-left text-base leading-7 text-toned sm:text-base'
    }"
  >
    <UCard
      variant="outline"
      :ui="{ root: 'overflow-hidden', body: 'p-0 sm:p-0' }"
    >
      <div class="grid sm:grid-cols-[1.1fr_0.9fr]">
        <div class="relative min-h-64 bg-muted sm:min-h-80">
          <img
            src="/images/consolacion-cover-photo.jpg"
            alt="Consolacion Municipal Hall and community artwork"
            class="absolute inset-0 size-full object-cover object-left"
            loading="lazy"
          >
        </div>
        <div class="bg-success-50/60 p-5 sm:p-7 lg:p-8">
          <h3 class="font-domine text-xl font-semibold leading-snug text-highlighted">
            Local destinations and stories
          </h3>
          <p class="mt-3 leading-7 text-toned">
            Explore places to visit and stories from the community.
          </p>

          <ul
            v-if="data.length"
            class="mt-5 divide-y divide-default"
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
            Explore tourism
          </UButton>
        </div>
      </div>
    </UCard>
  </UPageSection>
</template>
