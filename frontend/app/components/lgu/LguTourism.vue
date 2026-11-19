<script setup lang="ts">
const { data, error, pending } = await usePublicContent({
  kind: 'tourism',
  limit: 3
})
const stockImages = [
  '/images/stock-local-market.jpg',
  '/images/stock-community-park.jpg',
  '/images/stock-city-building.jpg'
]
</script>

<template>
  <section
    aria-labelledby="tourism-heading"
    class="border-t border-default bg-primary-50/40"
  >
    <UContainer class="py-10 sm:py-14">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2
            id="tourism-heading"
            class="font-domine text-3xl font-semibold text-highlighted"
          >
            Tourism and Local Experiences
          </h2>
          <p class="mt-2 leading-7 text-toned">
            Heritage and cultural highlights identified in municipal and provincial information.
          </p>
        </div>
        <UButton
          to="/tourism"
          variant="link"
          size="lg"
          trailing-icon="i-lucide-arrow-right"
        >
          Explore Consolacion
        </UButton>
      </div>

      <UAlert
        v-if="error"
        class="mt-6"
        color="error"
        variant="subtle"
        title="Tourism Information Is Temporarily Unavailable"
      />
      <UAlert
        v-else-if="!pending && !data?.length"
        class="mt-6"
        color="neutral"
        variant="subtle"
        title="No Tourism Entries Are Available"
        description="Contact the Municipal Tourism Office to confirm visitor information."
      />
      <div
        v-else
        class="mt-6 grid gap-4 md:grid-cols-3"
      >
        <article
          v-for="(item, index) in data"
          :key="item.id"
          class="overflow-hidden rounded-lg border border-default bg-default"
        >
          <div class="relative h-48">
            <img
              :src="item.image_url || stockImages[index]"
              :alt="item.image_url ? item.title : 'Illustrative Stock Photo'"
              loading="lazy"
              class="size-full object-cover"
            >
            <span
              v-if="!item.image_url"
              class="absolute bottom-3 right-3 rounded-full bg-black/55 px-3 py-1 text-xs font-medium text-white"
            >
              Illustrative Stock Photo
            </span>
          </div>
          <div class="p-5">
            <p class="text-sm text-muted">
              {{ item.category || 'Discover' }}
            </p>
            <h3 class="mt-2 font-domine text-xl font-semibold text-highlighted">
              <NuxtLink
                :to="publicContentPath(item)"
                class="hover:text-primary"
              >
                {{ item.title }}
              </NuxtLink>
            </h3>
            <p class="mt-2 line-clamp-3 leading-7 text-toned">
              {{ item.summary }}
            </p>
          </div>
        </article>
      </div>
    </UContainer>
  </section>
</template>
