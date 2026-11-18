<script setup lang="ts">
import { getStaticPublicContent } from '~/utils/static-public-content'

const slides = getStaticPublicContent('news').filter(item => item.featured).slice(0, 5)
const activeIndex = ref(0)
const activeSlide = computed(() => slides[activeIndex.value])
</script>

<template>
  <section
    aria-label="Featured news and events"
    aria-roledescription="carousel"
    class="grid min-h-[calc(100svh-var(--ui-header-height))] overflow-hidden bg-default lg:grid-cols-[1.05fr_0.95fr]"
  >
    <div class="relative h-[38svh] min-h-64 overflow-hidden bg-muted lg:h-auto lg:min-h-[calc(100svh-var(--ui-header-height))]">
      <img
        :src="activeSlide?.image_url || '/images/stock-community-park.jpg'"
        :alt="activeSlide?.image_url ? activeSlide.title : 'Illustrative stock photo of a public square'"
        fetchpriority="high"
        class="absolute inset-0 size-full object-cover"
      >
      <div class="absolute inset-0 bg-gradient-to-t from-black/55 via-black/5 to-black/20 lg:bg-gradient-to-r lg:from-black/20 lg:via-transparent lg:to-black/10" />
      <div class="absolute inset-x-0 bottom-0 flex flex-wrap items-end justify-between gap-3 p-5 sm:p-8 lg:p-10">
        <div class="flex flex-wrap gap-2">
          <span
            v-if="!activeSlide?.image_url"
            class="rounded-full bg-black/50 px-3 py-1.5 text-xs font-medium text-white"
          >
            Illustrative stock photo
          </span>
        </div>
        <span class="text-sm font-medium text-white">
          {{ activeIndex + 1 }} / {{ slides.length }}
        </span>
      </div>
    </div>

    <div
      v-if="activeSlide"
      role="group"
      aria-roledescription="slide"
      aria-live="polite"
      :aria-label="`${activeIndex + 1} of ${slides.length}: ${activeSlide.title}`"
      class="flex flex-col justify-center px-6 py-8 sm:px-10 sm:py-10 lg:px-14 lg:py-16 xl:px-20"
    >
      <div class="max-w-2xl">
        <div
          v-if="publicContentDate(activeSlide.record_date)"
          class="text-sm text-muted"
        >
          <time :datetime="activeSlide.record_date || undefined">
            {{ publicContentDate(activeSlide.record_date) }}
          </time>
        </div>
        <h1 class="mt-5 font-domine text-4xl font-semibold leading-tight text-highlighted sm:text-5xl lg:text-6xl">
          {{ activeSlide.title }}
        </h1>
        <p class="mt-5 max-w-xl text-base leading-7 text-toned sm:text-lg sm:leading-8">
          {{ activeSlide.summary }}
        </p>
      </div>

      <div class="mt-8 flex flex-wrap items-center justify-between gap-4 border-t border-default pt-5">
        <UButton
          :to="publicContentPath(activeSlide)"
          trailing-icon="i-lucide-arrow-right"
          size="lg"
        >
          Read this update
        </UButton>

        <div class="flex flex-wrap items-center gap-1">
          <button
            v-for="(slide, index) in slides"
            :key="slide.id"
            type="button"
            :aria-label="`Go to featured story ${index + 1}`"
            :aria-pressed="activeIndex === index"
            class="flex size-11 items-center justify-center rounded-full focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
            @click="activeIndex = index"
          >
            <span
              class="size-3 rounded-full"
              :class="activeIndex === index ? 'bg-primary' : 'border-2 border-muted'"
            />
          </button>
          <UButton
            icon="i-lucide-chevron-left"
            color="neutral"
            variant="outline"
            size="lg"
            aria-label="Previous featured story"
            @click="activeIndex = (activeIndex + slides.length - 1) % slides.length"
          />
          <UButton
            icon="i-lucide-chevron-right"
            color="neutral"
            variant="outline"
            size="lg"
            aria-label="Next featured story"
            @click="activeIndex = (activeIndex + 1) % slides.length"
          />
        </div>
      </div>
    </div>
    <div
      v-else
      class="flex items-center px-6 py-12 sm:px-10 lg:px-14 xl:px-20"
    >
      <UAlert
        color="neutral"
        variant="subtle"
        title="Featured updates are being prepared"
        description="Check back for verified news and event announcements."
      />
    </div>
  </section>
</template>
