<script setup lang="ts">
definePageMeta({ layout: 'transparency' })

const route = useRoute()
const archivePaths: Record<string, string> = {
  ordinance: '/transparency/ordinances',
  resolution: '/transparency/resolutions',
  memorandum: '/transparency/memorandums',
  executive_order: '/transparency/executive-orders',
  disclosure: '/transparency/full-disclosure',
  bid: '/transparency/bids-awards',
  form: '/transparency/forms'
}
const backTo = computed(
  () => archivePaths[String(route.query.kind)] || '/transparency'
)
</script>

<template>
  <LguPublicContentDetail
    :slug="String(route.params.slug)"
    :back-to="backTo"
  />
</template>
