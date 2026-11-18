<script setup lang="ts">
definePageMeta({ layout: 'about' })

const route = useRoute()
</script>

<template>
  <LguPublicContentDetail
    :slug="String(route.params.slug)"
    back-to="/about/actions"
  />
</template>
