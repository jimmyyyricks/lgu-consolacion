<script setup lang="ts">
const search = ref("");
const { data, error, pending } = await usePublicContent({
  kind: "tourism",
  limit: 100,
});
const stockImages = [
  "/images/stock-local-market.jpg",
  "/images/stock-community-park.jpg",
  "/images/stock-city-building.jpg",
];
const filteredStories = computed(() => {
  const term = search.value.trim().toLowerCase();
  if (!term) return data.value;
  return data.value.filter((item) =>
    `${item.title} ${item.summary} ${item.category || ""}`
      .toLowerCase()
      .includes(term),
  );
});

useSeoMeta({
  title: "Tourism | Municipality of Consolacion",
  description:
    "Explore local stories, community highlights, and visitor information from Consolacion, Cebu.",
});
</script>

<template>
  <div>
    <section
      aria-labelledby="tourism-heading"
      class="overflow-hidden bg-success-50"
    >
      <UContainer
        class="grid gap-10 py-12 sm:py-16 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)] lg:items-center lg:gap-14 lg:py-20"
      >
        <div>
          <h1
            id="tourism-heading"
            class="max-w-xl font-domine text-4xl font-semibold leading-tight text-success-950 sm:text-[2.75rem]"
          >
            Tourism in Consolacion
          </h1>
          <p
            class="mt-5 max-w-xl text-base leading-7 text-success-900 sm:text-lg"
          >
            Discover local stories, community highlights, and visitor
            information from Consolacion.
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <UButton
              to="#local-guides"
              size="lg"
              trailing-icon="i-lucide-arrow-down"
            >
              Explore Local Stories
            </UButton>
            <UButton to="/news" size="lg" color="neutral" variant="outline">
              What's Happening
            </UButton>
          </div>
          <p class="mt-5 text-base text-success-900">
            Official visitor updates from the Municipality of Consolacion.
          </p>
        </div>

        <figure
          class="overflow-hidden rounded-lg border border-success-200 bg-default shadow-sm"
        >
          <img
            src="/images/consolacion-cover-photo.jpg"
            alt="Consolacion municipal hall and community artwork"
            class="aspect-[2.27] w-full object-cover"
          />
          <figcaption class="sr-only">
            Consolacion, the Gateway to the North.
          </figcaption>
        </figure>
      </UContainer>
    </section>

    <section
      id="local-guides"
      aria-labelledby="local-guides-heading"
      class="scroll-mt-20"
    >
      <UContainer class="py-12 sm:py-16">
        <div
          class="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between"
        >
          <div>
            <h2
              id="local-guides-heading"
              class="font-domine text-3xl font-semibold leading-tight text-highlighted sm:text-4xl"
            >
              Local Guides and Community Stories
            </h2>
            <p class="mt-3 max-w-2xl text-base leading-7 text-toned sm:text-lg">
              Explore heritage and cultural highlights identified in municipal
              and provincial information.
            </p>
          </div>
          <UInput
            v-model="search"
            icon="i-lucide-search"
            placeholder="Search Local Stories"
            aria-label="Search Tourism Stories"
            size="lg"
            class="w-full sm:max-w-xs"
          />
        </div>

        <UAlert
          v-if="error"
          class="mt-8"
          color="error"
          variant="subtle"
          title="Tourism Information Is Temporarily Unavailable"
          description="Please try again later."
        />
        <div
          v-else-if="pending"
          class="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3"
          aria-label="Loading Tourism Stories"
        >
          <USkeleton v-for="item in 3" :key="item" class="h-96 w-full" />
        </div>
        <div
          v-else-if="filteredStories.length"
          class="mt-8 grid items-start gap-5 sm:grid-cols-2 lg:grid-cols-3"
        >
          <article v-for="(item, index) in filteredStories" :key="item.id">
            <UCard
              :ui="{
                root: 'rounded-lg shadow-none transition hover:border-primary/40 hover:shadow-sm',
                header: 'relative h-56 overflow-hidden p-0 sm:px-0',
                body: 'p-5 sm:p-5',
              }"
            >
              <template #header>
                <img
                  :src="
                    item.image_url || stockImages[index % stockImages.length]
                  "
                  :alt="
                    item.image_url ? item.title : 'Illustrative Stock Photo'
                  "
                  loading="lazy"
                  class="absolute inset-0 size-full object-cover transition duration-300 hover:scale-105"
                />
                <span
                  v-if="!item.image_url"
                  class="absolute bottom-3 left-3 rounded-full bg-default/95 px-3 py-1.5 text-sm font-medium text-toned"
                >
                  Illustrative Photo
                </span>
              </template>

              <div
                class="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-muted"
              >
                <span>{{ item.category || "Local story" }}</span>
              </div>
              <h3
                class="mt-2 font-domine text-xl font-semibold text-highlighted"
              >
                <NuxtLink
                  :to="publicContentPath(item)"
                  class="hover:text-primary focus-visible:outline-primary"
                >
                  {{ item.title }}
                </NuxtLink>
              </h3>
              <p class="mt-3 line-clamp-3 text-base leading-7 text-toned">
                {{ item.summary }}
              </p>
              <NuxtLink
                :to="publicContentPath(item)"
                class="mt-5 inline-flex items-center gap-2 font-medium text-primary hover:underline"
              >
                Read the Story
                <UIcon name="i-lucide-arrow-right" class="size-4" />
              </NuxtLink>
            </UCard>
          </article>
        </div>
        <UAlert
          v-else
          class="mt-8"
          color="neutral"
          variant="subtle"
          :title="
            search
              ? 'No Stories Match Your Search'
              : 'No Tourism Entries Are Available'
          "
          description="Contact the Municipal Tourism Office to confirm visitor information."
        />
      </UContainer>
    </section>

    <section
      id="visitor-info"
      aria-labelledby="visitor-info-heading"
      class="bg-primary-50/50"
    >
      <UContainer
        class="flex flex-col gap-6 py-10 sm:flex-row sm:items-center sm:justify-between sm:py-12"
      >
        <div class="max-w-2xl">
          <h2
            id="visitor-info-heading"
            class="font-domine text-2xl font-semibold text-highlighted sm:text-3xl"
          >
            Visitor Information and Events
          </h2>
          <p class="mt-2 leading-7 text-toned">
            Check official news and public notices for current community events
            and visitor updates.
          </p>
        </div>
        <div class="flex flex-wrap gap-3">
          <UButton to="/news" trailing-icon="i-lucide-arrow-right" size="lg">
            News and Events
          </UButton>
          <UButton
            to="/about/actions"
            color="neutral"
            variant="outline"
            size="lg"
          >
            Public Notices
          </UButton>
        </div>
      </UContainer>
    </section>
  </div>
</template>
