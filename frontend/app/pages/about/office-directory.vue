<script setup lang="ts">
import LguOfficeDirectory from '~/components/lgu/LguOfficeDirectory.vue'

definePageMeta({ layout: 'about' })

useSeoMeta({
  title: 'Office Directory | Municipality of Consolacion',
  description: 'Municipal office contact details and emergency and community hotlines.'
})
</script>

<template>
  <UPage>
    <UPageHeader
      title="Office Directory"
      description="Telephone numbers listed by the Municipality of Consolacion. Confirm details with the office before relying on them."
      :ui="{
        title: 'font-domine text-3xl font-semibold sm:text-4xl',
        container: 'mx-auto w-full max-w-(--ui-container) px-4 sm:px-6 lg:px-8'
      }"
    />
    <UPageBody>
      <LguOfficeDirectory />
    </UPageBody>
  </UPage>
</template>
