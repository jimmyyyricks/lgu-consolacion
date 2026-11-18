<script setup lang="ts">
const { data, error, pending } = await usePublicContent({
  kind: 'news',
  limit: 50
})
const latestNews = computed(() => data.value.filter(item => !item.featured).slice(0, 3))
const stockImages = [
  '/images/stock-community-park.jpg',
  '/images/stock-local-market.jpg',
  '/images/stock-city-building.jpg'
]
</script>

<template>
  <section
    aria-labelledby="latest-news-heading"
    class="border-b border-default"
  >
    <UContainer class="py-10 sm:py-14">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2
            id="latest-news-heading"
            class="font-domine text-3xl font-semibold text-highlighted"
          >
            News and events
          </h2>
        </div>
        <UButton
          to="/news"
          variant="link"
          size="lg"
          trailing-icon="i-lucide-arrow-right"
        >
          All news
        </UButton>
      </div>

      <div class="mt-7 grid items-start gap-8 lg:grid-cols-[minmax(0,2fr)_minmax(16rem,1fr)] lg:gap-12">
        <div>
          <UAlert
            v-if="error"
            color="error"
            variant="subtle"
            title="News is temporarily unavailable"
          />
          <div
            v-else-if="pending"
            class="space-y-4"
            aria-label="Loading news"
          >
            <USkeleton
              v-for="item in 3"
              :key="item"
              class="h-28 w-full"
            />
          </div>
          <div
            v-else-if="latestNews.length"
            class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3"
          >
            <article
              v-for="(item, index) in latestNews"
              :key="item.id"
              class="overflow-hidden rounded-lg border border-default bg-default"
            >
              <div class="relative h-44">
                <img
                  :src="item.image_url || stockImages[index]"
                  :alt="item.image_url ? item.title : 'Illustrative stock photo'"
                  loading="lazy"
                  class="size-full object-cover"
                >
                <span
                  v-if="!item.image_url"
                  class="absolute bottom-3 right-3 rounded-full bg-black/55 px-3 py-1 text-xs font-medium text-white"
                >
                  Illustrative stock photo
                </span>
              </div>
              <div class="p-4 sm:p-5">
                <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-muted">
                  <time
                    v-if="publicContentDate(item.record_date)"
                    :datetime="item.record_date || undefined"
                  >
                    {{ publicContentDate(item.record_date) }}
                  </time>
                  <span>{{ item.category || 'News' }}</span>
                </div>
                <h3 class="mt-2 font-domine text-xl font-semibold text-highlighted">
                  <NuxtLink
                    :to="publicContentPath(item)"
                    class="hover:text-primary focus-visible:outline-primary"
                  >
                    {{ item.title }}
                  </NuxtLink>
                </h3>
                <p class="mt-2 leading-7 text-toned">
                  {{ item.summary }}
                </p>
              </div>
            </article>
          </div>
          <UAlert
            v-else
            color="neutral"
            variant="subtle"
            title="No other news has been published"
          />
        </div>

        <LguActions />
      </div>
    </UContainer>
  </section>
</template>
