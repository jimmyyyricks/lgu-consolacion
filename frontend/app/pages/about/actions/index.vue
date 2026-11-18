<script setup lang="ts">
definePageMeta({ layout: 'about' })

useSeoMeta({
  title: 'Government Actions | Municipality of Consolacion',
  description:
    'Browse official actions, announcements, and issuances from the Municipality of Consolacion.'
})
</script>

<template>
  <LguPublicContentArchive
    kind="government_action"
    title="Government actions"
    description="Official announcements and actions from the municipal government."
  />
</template>
