<script setup lang="ts">
const route = useRoute()
</script>

<template>
  <LguPublicContentDetail
    :slug="String(route.params.slug)"
    back-to="/news"
  />
</template>
