<script setup lang="ts">
import { usePreferredReducedMotion, useWindowScroll } from "@vueuse/core";
import { useAuthStore } from "~/stores/auth";
import { useTokenRefresh } from "~/composables/useTokenRefresh";

const authStore = useAuthStore();
const { scheduleRefresh, cancelRefresh } = useTokenRefresh();
const { y } = useWindowScroll();
const reducedMotion = usePreferredReducedMotion();

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: reducedMotion.value === "reduce" ? "instant" : "smooth",
  });
}

useHead({
  meta: [
    { name: "viewport", content: "width=device-width, initial-scale=1" },
    { name: "color-scheme", content: "light dark" },
  ],
  link: [{ rel: "icon", href: "/favicon.ico" }],
  htmlAttrs: { lang: "en" },
});

useSeoMeta({
  title: "Municipality of Consolacion, Cebu",
  description:
    "Official information, public records, government updates, and tourism information from the Municipality of Consolacion.",
});

onMounted(() => {
  if (authStore.isAuthenticated && authStore.token) {
    scheduleRefresh(authStore.token);
  }
});

watch(
  () => authStore.token,
  (token) => {
    if (token) scheduleRefresh(token);
    else cancelRefresh();
  },
);

onUnmounted(cancelRefresh);
</script>

<template>
  <UApp>
    <NuxtLink
      to="#main-content"
      class="sr-only focus-visible:not-sr-only focus-visible:fixed focus-visible:left-4 focus-visible:top-4 focus-visible:z-[100] focus-visible:flex focus-visible:min-h-11 focus-visible:items-center focus-visible:bg-primary-700 focus-visible:px-4 focus-visible:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
    >
      Skip to main content
    </NuxtLink>
    <LguUtilityBar />
    <LguHeader />

    <UMain id="main-content" tabindex="-1">
      <NuxtErrorBoundary>
        <NuxtLayout>
          <NuxtPage />
        </NuxtLayout>

        <template #error="{ error, clearError }">
          <UContainer class="py-16">
            <UAlert
              color="error"
              title="This page could not be displayed"
              :description="error?.message || 'Please try again.'"
            />
            <UButton class="mt-4" size="lg" @click="clearError">
              Try again
            </UButton>
          </UContainer>
        </template>
      </NuxtErrorBoundary>
    </UMain>

    <LguSiteFooter />
    <Transition
      enter-active-class="transition-opacity duration-200 ease-out motion-reduce:duration-0"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200 ease-in motion-reduce:duration-0"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <UButton
        v-if="y > 300"
        icon="i-lucide-arrow-up"
        aria-label="Scroll to top"
        size="lg"
        class="fixed right-6 bottom-6 z-40 size-11 rounded-full"
        @click="scrollToTop"
      />
    </Transition>
  </UApp>
</template>
