<template>
  <div class="min-h-full">
    <LguWelcomeHero />
    <LguNewsCarousel />
    <LguServices />
    <section
      aria-labelledby="public-information-links-heading"
      class="border-y border-default bg-muted/30"
    >
      <UContainer
        class="flex flex-col items-center justify-between gap-4 py-5 sm:flex-row"
      >
        <h2
          id="public-information-links-heading"
          class="font-medium text-toned"
        >
          Transparency and Access to Information
        </h2>
        <div class="flex items-center gap-4">
          <NuxtLink
            to="/transparency"
            aria-label="View Municipal Transparency Information"
            class="flex min-h-10 min-w-10 items-center justify-center rounded-sm focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            <img
              src="/images/transparency-seal.svg"
              alt="Philippine Transparency Seal"
              width="140"
              height="140"
              class="size-20 object-contain sm:size-24"
              loading="lazy"
            />
          </NuxtLink>
          <a
            href="https://www.foi.gov.ph/"
            target="_blank"
            rel="noopener"
            aria-label="Open the Freedom of Information Portal in a New Tab"
            class="flex min-h-11 min-w-11 items-center justify-center rounded-sm focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            <img
              src="/images/foi-seal.png"
              alt="Freedom of Information Philippines"
              width="160"
              height="160"
              class="size-20 object-contain sm:size-24"
              loading="lazy"
            />
          </a>
        </div>
      </UContainer>
    </section>
    <LguToday />
    <LguPeoplesCorner />
  </div>
</template>
