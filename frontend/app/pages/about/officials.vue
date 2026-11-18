<script setup lang="ts">
definePageMeta({ layout: 'about' })

useSeoMeta({
  title: 'Municipal Officials | Municipality of Consolacion',
  description: 'Meet the elected members of Consolacion\'s 12th Sangguniang Bayan.'
})
</script>

<template>
  <UPage>
    <UPageHeader
      title="Municipal Officials"
      :ui="{
        title: 'font-domine text-3xl font-semibold sm:text-4xl',
        container: 'mx-auto w-full max-w-(--ui-container) px-4 sm:px-6 lg:px-8',
      }"
    />
    <UPageBody>
      <LguPublicServants />
    </UPageBody>
  </UPage>
</template>
