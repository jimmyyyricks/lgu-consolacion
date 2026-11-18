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
          Sangguniang Bayan activity notices
        </h2>
        <UButton
          to="/news"
          variant="link"
          trailing-icon="i-lucide-arrow-right"
          size="lg"
          class="text-primary-700 dark:text-primary-300"
        >
          All news
        </UButton>
      </div>
    </template>

    <div class="min-w-0">
      <UAlert
        v-if="error"
        color="error"
        variant="subtle"
        title="News is temporarily unavailable"
      />
      <UCard
        v-else-if="pending && !slides.length"
        aria-label="Loading latest news"
        variant="outline"
        :ui="{ body: 'grid gap-5 sm:grid-cols-2' }"
      >
        <USkeleton class="h-56 sm:h-72" />
        <div class="space-y-4 py-4">
          <USkeleton class="h-4 w-28" />
          <USkeleton class="h-10 w-full" />
          <USkeleton class="h-20 w-full" />
        </div>
      </UCard>
      <UAlert
        v-else-if="!slides.length"
        color="neutral"
        variant="subtle"
        title="No news has been published yet"
      />
      <div
        v-else
        class="relative"
      >
        <UCarousel
          :items="slides"
          :ui="{
            root: 'relative pb-12',
            item: 'px-0',
            container: 'ms-0',
            controls: 'absolute bottom-0 right-0 flex h-11 items-center',
            arrows: 'flex gap-2',
            prev: 'static size-11 translate-y-0',
            next: 'static size-11 translate-y-0'
          }"
          :prev="{ size: 'md', square: true, disabled: false }"
          :next="{ size: 'md', square: true, disabled: false }"
          :loop="slides.length > 1"
          :arrows="slides.length > 1"
          aria-label="Sangguniang Bayan activity notices"
          @select="activeIndex = $event"
        >
          <template #default="{ item, index }">
            <UCard
              as="article"
              variant="outline"
              :ui="{ body: 'grid p-0 sm:p-0 lg:min-h-[24rem] lg:grid-cols-[1.05fr_0.95fr]' }"
            >
              <div class="relative min-h-56 bg-muted sm:min-h-72 lg:min-h-full">
                <img
                  :src="item.image_url || stockImages[index % stockImages.length]"
                  :alt="item.image_url ? item.title : 'Illustrative stock photo'"
                  :fetchpriority="index === 0 ? 'high' : undefined"
                  :loading="index === 0 ? 'eager' : 'lazy'"
                  class="absolute inset-0 size-full object-cover"
                >
                <UBadge
                  v-if="!item.image_url"
                  color="neutral"
                  variant="solid"
                  class="absolute bottom-4 left-4"
                >
                  Illustrative stock photo
                </UBadge>
              </div>
              <div class="flex flex-col justify-center px-5 py-6 sm:px-7 lg:px-8">
                <div class="flex flex-wrap items-center gap-3 text-muted">
                  <time
                    v-if="publicContentDate(item.record_date)"
                    :datetime="item.record_date || undefined"
                  >
                    {{ publicContentDate(item.record_date) }}
                  </time>
                  <span v-if="item.category">{{ item.category }}</span>
                </div>
                <h3 class="mt-4 font-domine text-xl font-semibold leading-snug text-highlighted">
                  {{ item.title }}
                </h3>
                <p class="mt-4 line-clamp-4 leading-7 text-toned">
                  {{ item.summary }}
                </p>
                <UButton
                  :to="publicContentPath(item)"
                  trailing-icon="i-lucide-arrow-right"
                  size="lg"
                  class="mt-5 w-fit bg-primary-700 text-white hover:bg-primary-800"
                >
                  Read this update
                </UButton>
              </div>
            </UCard>
          </template>
        </UCarousel>
        <span class="absolute bottom-0 left-0 flex h-11 items-center text-muted">
          {{ activeIndex + 1 }} of {{ slides.length }}
        </span>
      </div>
    </div>
  </UPageSection>
</template>
