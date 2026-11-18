<script setup lang="ts">
const props = defineProps<{
  fileId: string
  title: string
}>()

const previewUrl = computed(
  () => `https://drive.google.com/file/d/${encodeURIComponent(props.fileId)}/preview`
)
const openUrl = computed(
  () => `https://drive.google.com/file/d/${encodeURIComponent(props.fileId)}/view`
)
</script>

<template>
  <section
    class="space-y-3"
    :aria-label="`${title} PDF`"
  >
    <iframe
      :src="previewUrl"
      :title="`${title} PDF preview`"
      loading="lazy"
      referrerpolicy="no-referrer"
      class="h-[70vh] min-h-96 w-full rounded-md border border-default bg-muted"
      allow="fullscreen"
    />
    <UButton
      :to="openUrl"
      target="_blank"
      rel="noopener noreferrer"
      color="neutral"
      variant="outline"
      size="lg"
      icon="i-lucide-external-link"
    >
      Open PDF in Google Drive
    </UButton>
  </section>
</template>
