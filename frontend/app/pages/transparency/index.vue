<script setup lang="ts">
definePageMeta({ layout: "transparency" });

useSeoMeta({
  title: "Transparency Portal | Municipality of Consolacion",
  description:
    "Access ordinances, resolutions, public disclosures, bids, awards, and official forms from Consolacion.",
});

const sections = [
  {
    title: "Ordinances",
    description: "Local laws enacted by the Sangguniang Bayan.",
    to: "/transparency/ordinances",
  },
  {
    title: "Resolutions",
    description: "Official resolutions and legislative actions.",
    to: "/transparency/resolutions",
  },
  {
    title: "Executive Orders",
    description: "Published executive issuances.",
    to: "/transparency/executive-orders",
  },
  {
    title: "Memoranda",
    description: "Published municipal memoranda.",
    to: "/transparency/memorandums",
  },
  {
    title: "Full Disclosure",
    description: "Publicly released financial and operational records.",
    to: "/transparency/full-disclosure",
  },
  {
    title: "Bids and Awards",
    description: "Procurement notices, bid documents, and award information.",
    to: "/transparency/bids-awards",
  },
  {
    title: "Downloadable Forms",
    description: "Official forms made available by municipal offices.",
    to: "/transparency/forms",
  },
];
</script>

<template>
  <UPage>
    <UPageHeader
      title="Transparency Portal"
      description="Find official municipal documents and public disclosures in one place."
      :ui="{
        title: 'font-domine text-3xl font-semibold sm:text-4xl',
        container: 'mx-auto w-full max-w-(--ui-container) px-4 sm:px-6 lg:px-8',
      }"
    >
    </UPageHeader>
    <UPageBody>
      <UContainer class="grid gap-4 py-8 sm:grid-cols-2 lg:grid-cols-3">
        <UCard v-for="section in sections" :key="section.to" class="h-full">
          <h2 class="font-domine text-xl font-semibold text-highlighted">
            <NuxtLink :to="section.to" class="hover:text-primary">
              {{ section.title }}
            </NuxtLink>
          </h2>
          <p class="mt-2 leading-7 text-toned">
            {{ section.description }}
          </p>
        </UCard>
      </UContainer>
    </UPageBody>
  </UPage>
</template>
