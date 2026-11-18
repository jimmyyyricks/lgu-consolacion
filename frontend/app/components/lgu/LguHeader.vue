<script setup lang="ts">
import { headerNavigation, siteRoutes } from "~/utils/site-navigation";
</script>

<template>
  <UHeader
    title="Municipality of Consolacion, Cebu"
    :to="siteRoutes.home"
    :ui="{
      root: 'bg-default border-b border-default shadow-none',
      container: 'gap-2 sm:gap-3',
      center: 'hidden xl:flex',
      toggle:
        'min-h-11 min-w-11 rounded-sm text-default focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-700',
      content: 'xl:hidden',
      overlay: 'xl:hidden',
      body: 'p-4 sm:p-6',
    }"
    :toggle="{
      color: 'neutral',
      variant: 'ghost',
      size: 'lg',
      class: 'min-h-11 min-w-11 rounded-sm',
    }"
  >
    <template #title>
      <div class="flex min-h-11 items-center gap-3">
        <img
          src="/images/lacion seal.jpg"
          alt="Municipality of Consolacion seal"
          class="size-10 shrink-0 rounded-sm object-cover sm:size-11"
        />
        <span class="flex flex-col leading-tight space-y-[-0.1rem]">
          <span class="text-sm font-medium text-toned">Municipality of</span>
          <span class="font-domine text-xl font-semibold text-highlighted">
            Consolacion
          </span>
        </span>
      </div>
    </template>

    <UNavigationMenu
      :items="headerNavigation"
      :ui="{
        link: 'min-h-11 text-sm uppercase text-default transition-colors duration-150 hover:text-primary-700 focus-visible:before:outline-2 focus-visible:before:outline-primary-700 motion-reduce:transition-none',
        viewport: 'w-[50rem] max-w-[calc(100vw-2rem)] shrink-0',
        childLink:
          'min-h-11 focus-visible:before:outline-2 focus-visible:before:outline-primary-700',
        childLinkDescription: 'text-muted',
      }"
      class="hidden xl:flex"
    />

    <template #body>
      <UNavigationMenu
        :items="headerNavigation"
        orientation="vertical"
        :ui="{
          link: 'min-h-11 text-sm uppercase text-default focus-visible:before:outline-2 focus-visible:before:outline-primary-700',
          childLink:
            'min-h-11 focus-visible:before:outline-2 focus-visible:before:outline-primary-700',
          childLinkDescription: 'text-muted',
        }"
        class="mb-4"
      />
      <NuxtLink
        :to="siteRoutes.login"
        class="mt-3 flex min-h-11 items-center px-3 text-sm font-medium text-primary-700 transition-colors duration-150 hover:text-primary-800 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-700 dark:text-primary-300 dark:hover:text-primary-200 motion-reduce:transition-none"
      >
        Staff sign in
      </NuxtLink>
    </template>
  </UHeader>
</template>
