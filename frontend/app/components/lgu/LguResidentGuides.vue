<script setup lang="ts">
interface QuickLink {
  icon: string;
  label: string;
  description: string;
  to: string;
}

const guides: QuickLink[] = [
  {
    label: "Find a municipal service",
    description:
      "Browse services and useful links for residents and businesses.",
    to: "/#services",
    icon: "i-lucide-search",
  },
  {
    label: "Get a municipal form",
    description: "Open forms published by municipal offices.",
    to: "/transparency/forms",
    icon: "i-lucide-file-down",
  },
  {
    label: "Read a public notice",
    description: "Check current municipal updates and public actions.",
    to: '/about/actions',
    icon: "i-lucide-megaphone",
  },
  {
    label: "Access public records",
    description: "Browse ordinances, resolutions, disclosures, and more.",
    to: "/transparency",
    icon: "i-lucide-files",
  },
];
</script>

<template>
  <UPageSection
    id="resident-guides"
    title="Resident guides"
    description="Clear starting points for common municipal information and services."
    aria-label="Resident guides"
    class="bg-muted/40"
    :ui="{
      container: 'gap-7 py-12 sm:gap-8 sm:py-14 lg:py-16',
      title: 'text-left font-domine text-3xl font-semibold leading-tight tracking-normal sm:text-4xl lg:text-4xl',
      description: 'mt-3 text-left text-base leading-7 text-toned sm:text-base'
    }"
  >
    <UPageGrid class="gap-4 lg:grid-cols-4">
      <UPageCard
        v-for="guide in guides"
        :key="guide.to"
        :to="guide.to"
        :icon="guide.icon"
        :title="guide.label"
        :description="guide.description"
        class="h-full [&>a]:absolute [&>a]:inset-0"
      >
        <template #title>
          <h3>{{ guide.label }}</h3>
        </template>
      </UPageCard>
    </UPageGrid>
  </UPageSection>
</template>
