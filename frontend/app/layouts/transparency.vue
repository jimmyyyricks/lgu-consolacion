<template>
  <div class="w-full">
    <UDashboardToolbar
      class="sticky z-40 bg-gray-200 px-0 backdrop-blur sm:px-0"
      :style="{ top: 'var(--ui-header-height)' }"
    >
      <UContainer class="w-full overflow-x-auto">
        <UNavigationMenu
          :items="navigationItems"
          aria-label="Public Record Categories"
          highlight
          class="w-max"
          :ui="{
            item: 'shrink-0',
            link: 'min-h-10 text-sm',
            linkLabel: 'whitespace-nowrap',
          }"
        />
      </UContainer>
    </UDashboardToolbar>
    <div class="min-w-0">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
const links = [
  { label: "Overview", to: "/transparency" },
  { label: "Ordinances", to: "/transparency/ordinances", kind: "ordinance" },
  { label: "Resolutions", to: "/transparency/resolutions", kind: "resolution" },
  {
    label: "Executive Orders",
    to: "/transparency/executive-orders",
    kind: "executive_order",
  },
  { label: "Memoranda", to: "/transparency/memorandums", kind: "memorandum" },
  {
    label: "Full Disclosure",
    to: "/transparency/full-disclosure",
    kind: "disclosure",
  },
  { label: "Bids and Awards", to: "/transparency/bids-awards", kind: "bid" },
  { label: "Forms", to: "/transparency/forms", kind: "form" },
];

const activeLink = computed(() => {
  const currentPage = links.find((link) => link.to === route.path);
  if (currentPage) return currentPage.to;
  if (
    !route.path.startsWith("/transparency/document/") ||
    typeof route.query.kind !== "string"
  ) {
    return undefined;
  }
  return links.find((link) => link.kind === route.query.kind)?.to;
});

const navigationItems = computed(() =>
  links.map((link) => ({
    ...link,
    active: activeLink.value === link.to,
  })),
);
</script>
