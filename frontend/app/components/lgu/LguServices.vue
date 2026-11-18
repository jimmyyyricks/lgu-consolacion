<script setup lang="ts">
import { publicServiceLinks } from "~/utils/services";

const search = ref("");
const matchingServices = computed(() => {
  const query = search.value.trim().toLowerCase();
  if (!query) return publicServiceLinks;
  return publicServiceLinks.filter((service) =>
    `${service.label} ${service.description}`.toLowerCase().includes(query),
  );
});
</script>

<template>
  <UPageSection
    id="services"
    aria-labelledby="services-heading"
    class="scroll-mt-32 bg-muted/40"
    :ui="{ container: 'gap-7 py-12 sm:gap-8 sm:py-14 lg:py-16' }"
  >
    <template #header>
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div class="max-w-3xl">
          <h2
            id="services-heading"
            class="font-domine text-3xl font-semibold leading-tight text-highlighted sm:text-4xl"
          >
            Services and Links
          </h2>
          <p class="mt-3 leading-7 text-toned">
            Find municipal forms, public notices, records and visitor information.
          </p>
        </div>
        <UInput
          v-model="search"
          icon="i-lucide-search"
          placeholder="Search services and links"
          aria-label="Search services and links"
          size="lg"
          class="w-full sm:w-72"
        />
      </div>
    </template>

    <UPageGrid
      v-if="matchingServices.length"
      class="gap-x-8 gap-y-0 lg:grid-cols-2"
    >
      <UPageFeature
        v-for="service in matchingServices"
        :key="service.to"
        :to="service.to"
        :title="service.label"
        :icon="service.icon"
        class="group min-h-24 items-center gap-4 border-t border-default py-4 [&_a]:absolute [&_a]:inset-0"
        :ui="{ leading: 'size-11 shrink-0', leadingIcon: 'size-6', wrapper: 'min-w-0 flex-1' }"
      >
        <div class="flex items-center justify-between gap-4">
          <span class="min-w-0">
            <span class="block font-semibold text-highlighted group-hover:text-primary">
              {{ service.label }}
            </span>
            <span class="mt-1 block leading-6 text-toned">
              {{ service.description }}
            </span>
          </span>
          <UIcon
            name="i-lucide-arrow-right"
            class="size-5 shrink-0 text-muted transition-transform group-hover:translate-x-1 group-hover:text-primary"
          />
        </div>
      </UPageFeature>
    </UPageGrid>
    <UAlert
      v-else
      color="neutral"
      variant="subtle"
      title="No matching service or link"
      description="Try a different search term."
    />
  </UPageSection>
</template>
