<script setup lang="ts">
import { municipalInformation } from "~/utils/municipal-information";
</script>

<template>
  <section
    id="about"
    aria-label="Municipal Vision, Mission, Mandate, and Objectives"
    class="bg-muted/40"
  >
    <UContainer class="py-6 sm:py-8 lg:py-10">
      <UPageGrid
        class="gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-2"
      >
        <UPageCard as="article" variant="solid" class="bg-primary-800">
          <template #body>
            <h3 class="font-domine text-xl font-semibold">Vision</h3>
            <p class="mt-3 leading-6">
              {{ municipalInformation.vision }}
            </p>
          </template>
        </UPageCard>
        <UPageCard as="article" variant="solid" class="bg-primary-800">
          <template #body>
            <h3 class="font-domine text-xl font-semibold">Mission</h3>
            <p class="mt-3 leading-6">
              {{ municipalInformation.mission }}
            </p>
          </template>
        </UPageCard>
        <UPageCard as="article" variant="subtle">
          <template #body>
            <h3 class="font-domine text-xl font-semibold">Mandate</h3>
            <p class="mt-3 leading-6">
              {{ municipalInformation.mandate }}
            </p>
          </template>
        </UPageCard>
        <UPageCard as="article" variant="subtle">
          <template #body>
            <h3 class="font-domine text-xl font-semibold">Objectives</h3>
            <p class="mt-3 leading-6">
              {{ municipalInformation.objectives }}
            </p>
          </template>
        </UPageCard>
      </UPageGrid>
    </UContainer>
  </section>
</template>
