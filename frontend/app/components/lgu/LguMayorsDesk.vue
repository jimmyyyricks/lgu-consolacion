<script setup lang="ts">
import { municipalInformation } from "~/utils/municipal-information";
</script>

<template>
  <section
    id="mayors-desk"
    aria-labelledby="mayors-desk-heading"
    class="overflow-hidden bg-primary-800 text-white"
  >
    <UContainer
      class="grid gap-10 py-12 sm:py-14 lg:grid-cols-[minmax(0,1.1fr)_minmax(18rem,0.9fr)] lg:items-center lg:gap-16 lg:py-16"
    >
      <div class="max-w-3xl">
        <h2
          id="mayors-desk-heading"
          class="font-domine text-3xl font-semibold leading-tight text-white sm:text-4xl"
        >
          A Message from the Vice Mayor
        </h2>
        <div class="mt-6 space-y-4 leading-7 text-white/90">
          <p
            v-for="paragraph in municipalInformation.viceMayorMessage"
            :key="paragraph"
          >
            {{ paragraph }}
          </p>
        </div>
        <p class="mt-6 font-semibold text-white">
          {{ municipalInformation.viceMayorName }}
          <span class="ml-2 font-normal text-white/75"
            >Vice Mayor / Presiding Officer</span
          >
        </p>
      </div>

      <div class="border-l-2 border-secondary-400 pl-6 sm:pl-8">
        <p class="font-domine text-2xl font-semibold leading-snug text-white">
          “Your voice and engagement are essential in building a more inclusive,
          healthy, and progressive Consolacion.”
        </p>
        <UButton
          to="/about#citizens-charter"
          color="secondary"
          size="lg"
          trailing-icon="i-lucide-arrow-right"
          class="mt-7 text-primary-950"
        >
          Read the Citizen's Charter
        </UButton>
      </div>
    </UContainer>
  </section>
</template>
