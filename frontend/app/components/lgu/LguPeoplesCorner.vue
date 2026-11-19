<script setup lang="ts">
const citizenCharterUrl = "/about#citizens-charter";
const feedbackEmail = "mailto:info@consolacion.gov.ph";
</script>

<template>
  <UPageSection
    id="peoples-corner"
    title="People's Corner"
    description="Find the right place to ask for help, access information, or share feedback."
    aria-label="People's Corner"
    :ui="{
      container: 'gap-7 py-12 sm:gap-8 sm:py-14 lg:py-16',
      title: 'text-left font-domine text-3xl font-semibold leading-tight tracking-normal sm:text-4xl lg:text-4xl',
      description: 'mt-3 text-left text-base leading-7 text-toned sm:text-base'
    }"
  >
    <div
      class="grid gap-5 lg:grid-cols-[minmax(0,1.25fr)_minmax(18rem,0.75fr)]"
    >
      <UPageGrid class="gap-4 lg:grid-cols-2">
        <UPageCard
          to="/#services"
          icon="i-lucide-life-buoy"
          title="Find a Service"
          variant="outline"
          class="[&>a]:absolute [&>a]:inset-0"
        >
          <template #title>
            <h3>
              Find a Service
            </h3>
          </template>
        </UPageCard>
        <UPageCard
          to="/transparency"
          icon="i-lucide-files"
          title="Request Public Information"
          variant="outline"
          class="[&>a]:absolute [&>a]:inset-0"
        >
          <template #title>
            <h3>
              Request Public Information
            </h3>
          </template>
        </UPageCard>
      </UPageGrid>

      <UCard
        variant="subtle"
        description="The municipal Citizen's Charter explains how to submit feedback or a complaint."
      >
        <template #title>
          <h3>Share feedback</h3>
        </template>
        <div class="flex flex-col items-start gap-2">
          <UButton
            :to="feedbackEmail"
            color="neutral"
            size="lg"
          >
            Email the Municipal Government
          </UButton>
          <UButton
            :to="citizenCharterUrl"
            color="neutral"
            variant="link"
            size="lg"
            trailing-icon="i-lucide-arrow-up-right"
            class="px-0"
          >
            Read the Citizen's Charter
          </UButton>
        </div>
      </UCard>
    </div>
  </UPageSection>
</template>
