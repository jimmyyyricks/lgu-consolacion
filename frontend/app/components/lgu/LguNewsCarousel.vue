<script setup lang="ts">
import { latestNewsSlides } from '~/utils/latest-news'

const { data, error, pending } = await usePublicContent({ kind: 'news', limit: 50 })
const slides = computed(() => latestNewsSlides(data.value, [], 5))
const activeIndex = ref(0)
const stockImages = [
  '/images/stock-community-park.jpg',
  '/images/stock-local-market.jpg',
  '/images/stock-city-building.jpg'
]
</script>

<template>
  <UPageSection
    aria-labelledby="news-carousel-heading"
    class="border-b border-default bg-muted/40"
    :ui="{ container: 'gap-5 py-12 sm:gap-5 sm:py-14 lg:py-16' }"
  >
    <template #header>
      <div class="flex flex-wrap items-center justify-between gap-3">
        <h2
          id="news-carousel-heading"
          class="font-domine text-3xl font-semibold leading-tight text-highlighted sm:text-4xl"
        >
          Latest Updates from the LGU
        </h2>
        <UButton
          to="/news"
          variant="outline"
          trailing-icon="i-lucide-arrow-right"
          size="lg"
        >
          All News
        </UButton>
      </div>
    </template>

    <div class="grid items-start gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)] lg:gap-8">
      <div class="min-w-0">
        <UAlert
          v-if="error"
          color="error"
          variant="subtle"
          title="News Is Temporarily Unavailable"
        />
        <UCard
          v-else-if="pending && !slides.length"
          aria-label="Loading Latest News"
          variant="outline"
          :ui="{ body: 'p-0' }"
        >
          <USkeleton class="aspect-[4/3] w-full" />
        </UCard>
        <UAlert
          v-else-if="!slides.length"
          color="neutral"
          variant="subtle"
          title="No News Has Been Published Yet"
        />
        <div
          v-else
          class="relative"
        >
          <UCarousel
            :items="slides"
            :ui="{
              root: 'relative',
              item: 'pe-4',
              container: 'ms-0',
              controls: 'absolute right-6 top-6 flex items-center',
              arrows: 'flex gap-16',
              prev: 'static size-8 translate-y-0',
              next: 'static size-8 translate-y-0'
            }"
            prev-icon="i-lucide-arrow-left"
            next-icon="i-lucide-arrow-right"
            :prev="{ color: 'neutral', size: 'sm', square: true }"
            :next="{ color: 'neutral', size: 'sm', square: true }"
            :loop="slides.length > 1"
            :arrows="slides.length > 1"
            aria-label="Latest Updates from the LGU"
            @select="activeIndex = $event"
          >
            <template #default="{ item, index }">
              <article class="relative aspect-[4/3] overflow-hidden rounded-xl bg-muted">
                <img
                  :src="item.image_url || stockImages[index % stockImages.length]"
                  :alt="item.image_url ? item.title : 'Illustrative Stock Photo'"
                  :fetchpriority="index === 0 ? 'high' : undefined"
                  :loading="index === 0 ? 'eager' : 'lazy'"
                  class="absolute inset-0 size-full object-cover"
                >
                <UBadge
                  v-if="!item.image_url"
                  color="neutral"
                  variant="solid"
                  class="absolute left-6 top-6"
                >
                  Illustrative Stock Photo
                </UBadge>
                <div
                  aria-hidden="true"
                  class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent"
                />
                <div class="absolute inset-x-0 bottom-0 p-6 text-left text-white">
                  <div class="flex flex-wrap items-center gap-3 text-sm text-white/80">
                    <time
                      v-if="publicContentDate(item.record_date)"
                      :datetime="item.record_date || undefined"
                    >
                      {{ publicContentDate(item.record_date) }}
                    </time>
                    <span v-if="item.category">{{ item.category }}</span>
                  </div>
                  <h3 class="mt-2 font-domine text-xl font-semibold leading-snug sm:text-2xl">
                    {{ item.title }}
                  </h3>
                  <p class="mt-2 line-clamp-2 leading-6 text-white/90">
                    {{ item.summary }}
                  </p>
                  <UButton
                    :to="publicContentPath(item)"
                    trailing-icon="i-lucide-arrow-right"
                    size="md"
                    class="mt-3 w-fit bg-white text-neutral-950 hover:bg-neutral-100"
                  >
                    Read This Update
                  </UButton>
                </div>
              </article>
            </template>
          </UCarousel>
          <span
            v-if="slides.length > 1"
            aria-live="polite"
            aria-atomic="true"
            class="absolute right-16 top-6 z-10 rounded-md bg-black/60 px-2 py-1 text-sm font-medium tabular-nums text-white"
          >
            {{ activeIndex + 1 }} of {{ slides.length }}
          </span>
        </div>
      </div>
      <LguActions />
    </div>
  </UPageSection>
</template>
