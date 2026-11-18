<template>
  <div class="w-full">
    <UDashboardToolbar
      class="sticky z-40 bg-gray-200 px-0 backdrop-blur sm:px-0"
      :style="{ top: 'var(--ui-header-height)' }"
    >
      <UContainer class="w-full overflow-x-auto">
        <UNavigationMenu
          :items="navigationItems"
          aria-label="About Consolacion sections"
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
  { label: "Citizen's Charter", to: "/about" },
  { label: "Office of the Mayor", to: "/about/mayor" },
  { label: "Office of the Vice Mayor", to: "/about/vice-mayor" },
  { label: "Municipal Officials", to: "/about/officials" },
  { label: "Office Directory", to: "/about/office-directory" },
  { label: "Government Actions", to: "/about/actions" },
];

const activeLink = computed(() => {
  const currentPath = `${route.path}${route.hash}`;
  const currentLink = links.find((link) => link.to === currentPath);
  if (currentLink) return currentLink.to;
  if (route.path.startsWith("/about/actions/")) return "/about/actions";
  return links.find((link) => link.to === route.path)?.to;
});

const navigationItems = computed(() =>
  links.map((link) => ({
    ...link,
    active: activeLink.value === link.to,
  })),
);
</script>
