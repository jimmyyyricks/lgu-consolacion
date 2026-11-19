<script setup lang="ts">
import { municipalInformation } from "~/utils/municipal-information";
import { footerColumns, siteRoutes } from "~/utils/site-navigation";
</script>

<template>
  <UFooter
    :ui="{
      root: 'bg-primary-800 text-white',
      top: 'border-t border-white/15 py-0 lg:py-0',
      container: 'border-t border-white/20 py-4 sm:py-5',
      left: 'justify-start text-sm text-white/85',
      center: 'text-sm text-white/70',
      right: 'justify-end',
    }"
  >
    <template #top>
      <UContainer class="py-9 sm:py-12">
        <UFooterColumns
          :columns="footerColumns"
          :ui="{
            root: 'grid gap-8 lg:grid-cols-[minmax(14rem,0.8fr)_minmax(0,2fr)] xl:grid-cols-[minmax(14rem,0.8fr)_minmax(0,2fr)]',
            left: 'mb-0',
            center:
              'grid grid-cols-2 grid-flow-row gap-x-6 gap-y-8 sm:grid-cols-3 lg:grid-flow-row xl:col-span-1',
            label:
              'px-0 text-sm font-medium text-white uppercase tracking-wider',
            list: 'space-y-[-0.125rem] mt-4',
            link: 'min-h-10 text-sm text-white/85 hover:text-white sm:min-h-8',
          }"
        >
          <template #left>
            <div class="max-w-sm">
              <NuxtLink
                :to="siteRoutes.home"
                class="inline-flex items-center gap-3 rounded-md focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-secondary"
              >
                <img
                  src="/images/lacion seal.jpg"
                  alt=""
                  class="size-12 rounded-full object-cover"
                />
                <span class="flex flex-col leading-tight">
                  <span class="text-sm text-white/85">Municipality of</span>
                  <span class="font-domine text-xl font-semibold text-white"
                    >Consolacion</span
                  >
                </span>
              </NuxtLink>
              <p class="mt-4 leading-7 text-white/85 leading-relaxed text-sm">
                Official municipal information for residents, businesses and
                visitors.
              </p>
              <p class="mt-3 leading-7 text-white/85 text-sm">
                <a
                  href="tel:+63322392908"
                  class="underline-offset-4 hover:underline"
                >
                  {{ municipalInformation.phone }}
                </a>
                <br />
                <a
                  href="mailto:info@consolacion.gov.ph"
                  class="underline-offset-4 hover:underline"
                >
                  {{ municipalInformation.email }}
                </a>
              </p>
              <p class="mt-3 leading-7 text-white/85 text-sm">
                Consolacion, Cebu
              </p>
            </div>
          </template>
        </UFooterColumns>
      </UContainer>
    </template>

    <template #left>
      © {{ new Date().getFullYear() }} Municipality of Consolacion, Cebu
    </template>

    <template #default>
      Illustrative imagery is identified where used.
    </template>

    <template #right>
      <NuxtLink
        :to="siteRoutes.login"
        class="min-h-11 content-center underline-offset-4 hover:text-white hover:underline"
      >
        Staff Sign In
      </NuxtLink>
    </template>
  </UFooter>
</template>
