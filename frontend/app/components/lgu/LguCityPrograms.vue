<script setup lang="ts">
const citizenCharterUrl = '/about#citizens-charter'

const programs = [
  {
    name: 'Government Internship Program',
    category: 'Public Employment',
    description: 'A 3–6 month work opportunity for young people interested in public service.',
    icon: 'i-lucide-briefcase-business'
  },
  {
    name: 'Special Program for Employment of Students',
    category: 'Student Employment',
    description: 'Student employment assistance listed in the municipal Citizen\'s Charter.',
    icon: 'i-lucide-graduation-cap'
  },
  {
    name: 'Hi-Speed Sewing Livelihood Program',
    category: 'Livelihood',
    description: 'A job-generation and livelihood program offered through the local government.',
    icon: 'i-lucide-scissors'
  }
]
</script>

<template>
  <LguSection
    id="city-programs"
    title="Municipal Programs"
    description="Employment and livelihood initiatives listed in the Consolacion Citizen's Charter."
  >
    <template #actions>
      <UButton
        :to="citizenCharterUrl"
        variant="link"
        size="lg"
        trailing-icon="i-lucide-arrow-up-right"
      >
        View the Citizen's Charter
      </UButton>
    </template>

    <UPageGrid class="gap-4 sm:grid-cols-1 md:grid-cols-3">
      <UPageCard
        v-for="program in programs"
        :key="program.name"
        variant="outline"
        :icon="program.icon"
        :ui="{ leadingIcon: 'size-7', body: 'w-full' }"
      >
        <template #body>
          <p class="mt-3 font-semibold text-primary">
            {{ program.category }}
          </p>
          <h3
            class="mt-2 font-domine text-xl font-semibold leading-snug text-highlighted"
          >
            {{ program.name }}
          </h3>
          <p class="mt-3 leading-7 text-toned">
            {{ program.description }}
          </p>
        </template>
        <template #footer>
          <UButton
            :to="citizenCharterUrl"
            variant="link"
            size="lg"
            trailing-icon="i-lucide-arrow-up-right"
            class="px-0"
          >
            Program Details
          </UButton>
        </template>
      </UPageCard>
    </UPageGrid>
  </LguSection>
</template>
