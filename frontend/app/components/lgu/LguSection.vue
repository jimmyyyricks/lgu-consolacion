<script setup lang="ts">
withDefaults(defineProps<{
  id: string
  title: string
  description?: string
  tone?: 'default' | 'muted' | 'primary'
}>(), {
  tone: 'default'
})
</script>

<template>
  <section
    :id="id"
    :aria-labelledby="`${id}-heading`"
    :class="{
      'bg-muted/40': tone === 'muted',
      'bg-primary-50 dark:bg-primary-950/40': tone === 'primary',
      'bg-default': tone === 'default'
    }"
  >
    <UContainer class="py-12 sm:py-14 lg:py-16">
      <div class="mb-7 flex flex-wrap items-end justify-between gap-4 sm:mb-8">
        <div class="max-w-3xl">
          <h2
            :id="`${id}-heading`"
            class="font-domine text-3xl font-semibold leading-tight text-highlighted sm:text-4xl"
          >
            {{ title }}
          </h2>
          <p
            v-if="description"
            class="mt-3 leading-7 text-toned"
          >
            {{ description }}
          </p>
        </div>
        <slot name="actions" />
      </div>
      <slot />
    </UContainer>
  </section>
</template>
