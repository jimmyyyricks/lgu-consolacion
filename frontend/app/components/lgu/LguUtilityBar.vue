<script setup lang="ts">
import { siteRoutes } from "~/utils/site-navigation";
</script>

<template>
  <div class="border-b border-default bg-muted text-default">
    <UContainer
      class="flex min-h-11 items-center justify-between gap-4 text-sm"
    >
      <p class="truncate">Consolacion, Cebu · 6001</p>
      <NuxtLink
        :to="siteRoutes.login"
        class="flex min-h-11 shrink-0 items-center font-medium text-primary-700 underline-offset-4 transition-colors duration-150 hover:text-primary-800 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-700 dark:text-primary-300 dark:hover:text-primary-200 motion-reduce:transition-none"
      >
        Staff Sign In
      </NuxtLink>
    </UContainer>
  </div>
</template>
