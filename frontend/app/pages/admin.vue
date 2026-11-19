<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const links = [
  {
    label: 'Public Content',
    icon: 'i-lucide-newspaper',
    to: '/admin/content'
  }
]
</script>

<template>
  <div class="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
    <header class="mb-6 border-b border-default pb-4">
      <h1 class="font-domine text-2xl font-semibold text-highlighted">
        Editorial Workspace
      </h1>
      <UNavigationMenu
        :items="links"
        class="mt-3"
      />
    </header>
    <NuxtPage />
  </div>
</template>
