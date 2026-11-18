<script setup lang="ts">
import type { ButtonProps } from '@nuxt/ui'
import municipalHallImage from '~/assets/consolacion-govt.jpg'

const quickLinks = [
  {
    label: 'Find a municipal service',
    description: 'Browse services and useful links for residents and businesses.',
    to: '/#services',
    icon: 'i-lucide-search'
  },
  {
    label: 'Get a municipal form',
    description: 'Open forms published by municipal offices.',
    to: '/transparency/forms',
    icon: 'i-lucide-file-down'
  },
  {
    label: 'Read a public notice',
    description: 'Check current municipal updates and public actions.',
    to: '/about/actions',
    icon: 'i-lucide-megaphone'
  },
  {
    label: 'Access public records',
    description: 'Browse ordinances, resolutions, disclosures, and more.',
    to: '/transparency',
    icon: 'i-lucide-files'
  }
]

const quickActions: ButtonProps[] = [
  {
    label: 'Services and links',
    to: '/#services',
    ui: { base: 'bg-primary-700 text-white hover:bg-primary-800' }
  },
  {
    label: 'Government updates',
    to: '/about/actions',
    color: 'neutral',
    variant: 'outline',
    ui: { base: 'bg-white text-primary-950 hover:bg-primary-50' }
  },
  {
    label: 'Public records',
    to: '/transparency',
    color: 'neutral',
    ui: { base: 'bg-neutral-900 text-white hover:bg-neutral-800' }
  }
]
</script>

<template>
  <UPageHero
    as="section"
    title="Welcome to Consolacion"
    description="Official services, public information and updates from the Municipality of Consolacion, Cebu."
    :links="quickActions"
    class="relative isolate overflow-hidden bg-default"
    :ui="{
      container: 'relative flex min-h-[calc(100svh-var(--ui-header-height)-2.8125rem)] justify-center pt-20 pb-12 sm:pt-24 sm:pb-14 lg:flex lg:pt-28 lg:pb-16',
      wrapper: 'mx-auto w-full text-center',
      title: 'text-balance font-domine text-4xl font-semibold leading-[1.05] tracking-normal text-white [text-shadow:0_2px_8px_rgba(0,0,0,0.8)] sm:text-6xl lg:text-7xl',
      description: 'mx-auto mt-6 max-w-2xl text-pretty text-base leading-7 text-white/90 [text-shadow:0_1px_4px_rgba(0,0,0,0.9)] sm:mt-7 sm:text-base',
      body: 'mt-10 sm:mt-12',
      footer: 'mt-8 sm:mt-10',
      links: 'mx-auto flex w-full max-w-xl flex-col gap-3 sm:flex-row sm:flex-wrap sm:justify-center'
    }"
  >
    <template #top>
      <div class="absolute inset-x-0 top-0 h-[38rem] sm:h-full">
        <img
          :src="municipalHallImage"
          alt="Consolacion Municipal Hall"
          fetchpriority="high"
          class="absolute inset-0 size-full object-cover object-[center_42%] sm:object-center"
        >
        <div
          aria-hidden="true"
          class="absolute inset-0 bg-neutral-950/80 backdrop-blur-[2px]"
        />
        <div
          aria-hidden="true"
          class="absolute inset-0 bg-gradient-to-b from-transparent from-40% to-default"
        />
      </div>
    </template>

    <template #title>
      Welcome to<br>Consolacion
    </template>

    <template #body>
      <div
        id="resident-guides"
        role="region"
        aria-label="Quick links"
      >
        <UPageGrid class="gap-4 lg:grid-cols-4">
          <UPageCard
            v-for="link in quickLinks"
            :key="link.to"
            :to="link.to"
            :icon="link.icon"
            :title="link.label"
            :description="link.description"
            class="h-full text-left [&>a]:absolute [&>a]:inset-0"
          >
            <template #title>
              <h2>{{ link.label }}</h2>
            </template>
          </UPageCard>
        </UPageGrid>
      </div>
    </template>
  </UPageHero>
</template>
