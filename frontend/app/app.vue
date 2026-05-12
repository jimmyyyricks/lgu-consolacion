<style>
@import url("https://fonts.googleapis.com/css2?family=Domine:wght@400;500;600;700&display=swap");

.font-domine {
  font-family: "Domine", serif;
}
</style>

<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";
import { useTokenRefresh } from "~/composables/useTokenRefresh";
import { useUserActivity } from "~/composables/useUserActivity";

const authStore = useAuthStore();
const { scheduleRefresh, cancelRefresh } = useTokenRefresh();
const { trackActivity } = useUserActivity();

useHead({
  meta: [
    { name: "viewport", content: "width=device-width, initial-scale=1" },
    { name: "color-scheme", content: "light" },
  ],
  link: [{ rel: "icon", href: "/favicon.ico" }],
  htmlAttrs: {
    lang: "en",
    class: "light",
  },
});

const colorMode = useColorMode();
const appConfig = useAppConfig();
const route = useRoute();

onMounted(() => {
  // Schedule proactive token refresh if already authenticated
  if (authStore.isAuthenticated && authStore.token) {
    scheduleRefresh(authStore.token);
  }
});

// Re-schedule whenever token is updated (login or refresh)
watch(
  () => authStore.token,
  (newToken) => {
    if (newToken) {
      scheduleRefresh(newToken);
    } else {
      cancelRefresh();
    }
  },
);

onUnmounted(() => {
  cancelRefresh();
});

onMounted(() => {
  // Load persisted accent colors, but force light mode
  const saved = localStorage.getItem("lgu:theme");
  if (saved) {
    try {
      const theme = JSON.parse(saved);
      if (theme.primary) appConfig.ui.colors.primary = theme.primary;
      if (theme.neutral) appConfig.ui.colors.neutral = theme.neutral;
    } catch {}
  }

  colorMode.preference = "light";
  document.documentElement.classList.remove("dark");
  document.documentElement.classList.add("light");
});

const title = "Municipality of Consolacion";
const description = "The central hub for Consolacion.";

useSeoMeta({
  title,
  description,
  ogTitle: title,
  ogDescription: description,
});

// Track page visits when route changes
watch(
  () => route.path,
  (newPath, oldPath) => {
    if (!authStore.isAuthenticated) return;

    // Skip tracking for login page and initial load
    if (newPath === "/login" || !oldPath) return;

    // Determine activity type and details based on route
    const pathParts = newPath.split("/").filter(Boolean);
    let activityType:
      | "entity_view"
      | "page_visit"
      | "quick_create"
      | "admin_action" = "page_visit";
    let entityName: string | undefined;
    let pageLabel: string | undefined;

    if (pathParts.length >= 1) {
      const firstPart = pathParts[0];

      if (!firstPart) return;

      // Check if it's an entity route
      if (
        [
          "asset",
          "asset_class",
          "location",
          "work_order",
          "maintenance_request",
          "purchase_order",
          "purchase_requisition",
          "item",
          "vendor",
        ].includes(firstPart)
      ) {
        activityType = "entity_view";
        entityName = firstPart;
        pageLabel = firstPart
          .replace(/_/g, " ")
          .replace(/\b\w/g, (l) => l.toUpperCase());
      } else if (firstPart === "admin") {
        activityType = "admin_action";
        pageLabel = "Administration";
      } else if (firstPart === "dashboard") {
        pageLabel = "Dashboard";
      } else if (firstPart === "calendar") {
        pageLabel = "PM Calendar";
      } else if (firstPart === "workflow") {
        pageLabel = "Workflow";
      } else if (firstPart === "reports") {
        pageLabel = "Reports";
      } else if (firstPart === "settings") {
        pageLabel = "Settings";
      } else if (firstPart === "profile") {
        pageLabel = "Profile";
      } else if (firstPart === "import-export") {
        pageLabel = "Import & Export";
      } else if (firstPart === "model-editor") {
        pageLabel = "Data Model Editor";
      }
    }

    // Track the activity
    trackActivity(activityType, {
      entityName,
      pagePath: newPath,
      pageLabel,
    });
  },
);

// Global error handler — catches unhandled Vue errors
const appError = ref<{ statusCode?: number; message?: string } | null>(null);

const handleError = () => {
  appError.value = null;
  clearError({ redirect: "/" });
};

useNuxtApp().vueApp.config.errorHandler = (err: any, _instance, info) => {
  console.error(`[Global Error] ${info}:`, err);
};
</script>

<template>
  <UApp>
    <UMain>
      <!-- Global error boundary -->
      <NuxtErrorBoundary
        @error="(err) => console.error('[ErrorBoundary]', err)"
      >
        <NuxtLayout>
          <NuxtPage />
        </NuxtLayout>

        <template
          #error="{ error: boundaryError, clearError: clearBoundaryError }"
        >
          <div
            class="flex flex-col items-center justify-center min-h-[60vh] gap-4 px-4"
          >
            <UIcon
              name="i-lucide-alert-triangle"
              class="h-16 w-16 text-red-500"
            />
            <h2 class="text-xl font-semibold">Something went wrong</h2>
            <p class="text-muted text-center max-w-md">
              {{ boundaryError?.message || "An unexpected error occurred." }}
            </p>
            <div class="flex gap-2">
              <UButton @click="clearBoundaryError" variant="outline">
                Try Again
              </UButton>
              <UButton @click="navigateTo('/')"> Go Home </UButton>
            </div>
          </div>
        </template>
      </NuxtErrorBoundary>

      <!-- Global modals -->
      <DeleteModal />
      <ConfirmModal />
      <EntityModal />
    </UMain>
  </UApp>
</template>
