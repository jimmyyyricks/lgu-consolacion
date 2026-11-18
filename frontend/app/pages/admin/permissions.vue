<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
await navigateTo('/admin/content', { replace: true })
</script>
