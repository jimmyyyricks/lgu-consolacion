<script setup lang="ts">
const officials = [
  { name: 'Hon. Joannes P. Alegado, MD', role: 'Vice Mayor / Presiding Officer', initials: 'JA' },
  { name: 'Hon. Leo B. Napuli', role: 'Sangguniang Bayan Member', initials: 'LN' },
  { name: 'Hon. Bienvenido G. Ermac', role: 'Sangguniang Bayan Member', initials: 'BE' },
  { name: 'Hon. Victor C. Maglasang, Jr.', role: 'Sangguniang Bayan Member', initials: 'VM' },
  { name: 'Hon. Fredelino T. Herrera', role: 'Sangguniang Bayan Member', initials: 'FH' },
  { name: 'Hon. Miko Mark Z. Ouano', role: 'Sangguniang Bayan Member', initials: 'MO' },
  { name: 'Hon. Elenito P. Palang', role: 'Sangguniang Bayan Member', initials: 'EP' },
  { name: 'Hon. Maria Analee Gungob-Corpin', role: 'Sangguniang Bayan Member', initials: 'MG' },
  { name: 'Hon. Reynaldo M. Pepito, Jr.', role: 'Sangguniang Bayan Member', initials: 'RP' },
  { name: 'Hon. Wesley M. Alimoren', role: 'Sangguniang Bayan Member', initials: 'WA' },
  { name: 'Hon. Shella A. Carpina', role: 'Sangguniang Bayan Member', initials: 'SC' }
]

const carousel = ref()
const carouselReady = ref(false)
const canScrollPrev = ref(false)
const canScrollNext = ref(false)

function syncCarouselControls() {
  const api = carousel.value?.emblaApi
  if (!api) return

  canScrollPrev.value = api.canScrollPrev()
  canScrollNext.value = api.canScrollNext()
  carouselReady.value = true
}

onMounted(() => {
  const api = carousel.value?.emblaApi
  if (!api) return

  api.on('select', syncCarouselControls)
  api.on('reInit', syncCarouselControls)
  syncCarouselControls()
})

onBeforeUnmount(() => {
  const api = carousel.value?.emblaApi
  if (!api) return

  api.off('select', syncCarouselControls)
  api.off('reInit', syncCarouselControls)
})
</script>

<template>
  <LguSection
    id="public-servants"
    title="Sangguniang Bayan Members"
    description="Meet the 12th Sangguniang Bayan serving the 2025–2028 term."
    tone="muted"
  >
    <div class="relative">
      <UCarousel
        ref="carousel"
        :items="officials"
        :ui="{
          root: 'relative pb-12',
          item: 'basis-4/5 sm:basis-1/2 lg:basis-1/3',
          container: 'ms-0'
        }"
        aria-label="Consolacion Public Servants"
      >
        <template #default="{ item }">
          <UCard
            variant="outline"
            :ui="{ root: 'h-full bg-default', body: 'flex min-h-52 items-center gap-4 p-5 sm:p-6' }"
          >
            <UAvatar
              :text="item.initials"
              :alt="item.name"
              size="2xl"
              color="primary"
            />
            <div class="min-w-0">
              <h3 class="font-domine text-xl font-semibold leading-snug text-highlighted">
                {{ item.name }}
              </h3>
              <p class="mt-2 leading-6 text-toned">
                {{ item.role }}
              </p>
            </div>
          </UCard>
        </template>
      </UCarousel>
      <div
        role="group"
        aria-label="Officials Carousel Controls"
        class="absolute bottom-0 right-0 flex h-11 items-center gap-2"
      >
        <UButton
          :disabled="carouselReady && !canScrollPrev"
          icon="i-lucide-arrow-left"
          color="neutral"
          variant="outline"
          size="md"
          square
          aria-label="Previous Officials"
          class="static size-11 translate-y-0"
          @click="carousel?.emblaApi?.scrollPrev()"
        />
        <UButton
          :disabled="carouselReady && !canScrollNext"
          icon="i-lucide-arrow-right"
          color="neutral"
          variant="outline"
          size="md"
          square
          aria-label="Next Officials"
          class="static size-11 translate-y-0"
          @click="carousel?.emblaApi?.scrollNext()"
        />
      </div>
    </div>
  </LguSection>
</template>
