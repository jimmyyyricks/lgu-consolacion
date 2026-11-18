<script setup lang="ts">
definePageMeta({ layout: "about" });

useSeoMeta({
  title: "About Consolacion | Municipality of Consolacion",
  description:
    "Learn about Consolacion's government, municipal offices, programs, and service commitments.",
});
</script>

<template>
  <UPage>
    <UPageHeader
      title="About Consolacion"
      description="Consolacion is a municipality in the Province of Cebu. Its official vision and mission are set out in the municipal Citizen's Charter."
      :ui="{
        title: 'font-domine text-3xl font-semibold sm:text-4xl',
        container: 'mx-auto w-full max-w-(--ui-container) px-4 sm:px-6 lg:px-8',
      }"
    />
    <UPageBody>
      <LguAbout />
      <LguCityPrograms />
      <LguCharterDetails />
    </UPageBody>
  </UPage>
</template>
