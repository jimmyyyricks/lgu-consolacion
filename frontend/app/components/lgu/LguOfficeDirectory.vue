<script setup lang="ts">
import {
  citizensCharter,
  municipalInformation,
  municipalOfficeDirectory,
} from "~/utils/municipal-information";

const hotlineGroup = "Emergency and community services";
const hotlines = municipalOfficeDirectory.filter(
  (item) => item.group === hotlineGroup,
);
const groups = [
  ...new Set(municipalOfficeDirectory.map((item) => item.group)),
].filter((group) => group !== hotlineGroup);
const phoneNumbers = (phone: string) =>
  phone.split("/").map((number) => number.trim());
const telephoneHref = (phone: string) => `tel:${phone.replace(/[^0-9+]/g, "")}`;
</script>

<template>
  <section aria-label="Office directory">
    <UContainer class="py-8 sm:py-12">
      <UPageGrid class="mb-7 gap-4 sm:grid-cols-3">
        <UCard variant="outline">
          <p class="font-medium text-highlighted">Municipal Hall</p>
          <p class="mt-1 text-toned">
            {{ municipalInformation.address }}
          </p>
        </UCard>
        <UCard variant="outline">
          <p class="font-medium text-highlighted">Telephone</p>
          <a
            class="mt-1 inline-block text-primary underline-offset-4 hover:underline"
            href="tel:+63322392908"
          >
            {{ municipalInformation.phone }}
          </a>
        </UCard>
        <UCard variant="outline">
          <p class="font-medium text-highlighted">Email</p>
          <a
            class="mt-1 inline-block text-primary underline-offset-4 hover:underline"
            :href="`mailto:${municipalInformation.email}`"
          >
            {{ municipalInformation.email }}
          </a>
        </UCard>
      </UPageGrid>

      <section aria-labelledby="emergency-hotlines-heading" class="mb-8">
        <div class="mb-4">
          <h2
            id="emergency-hotlines-heading"
            class="font-domine text-2xl font-semibold text-highlighted"
          >
            Emergency and community hotlines
          </h2>
          <p class="mt-2 leading-7 text-toned">
            Select a number to call the listed municipal or community service.
          </p>
        </div>
        <UPageGrid class="gap-4">
          <UCard
            v-for="entry in hotlines"
            :key="entry.office"
            variant="outline"
          >
            <div class="flex items-start gap-3">
              <UIcon
                name="i-lucide-phone"
                class="mt-1 size-5 shrink-0 text-primary"
              />
              <div class="min-w-0">
                <h3 class="font-semibold text-highlighted">
                  {{ entry.office }}
                </h3>
                <p class="mt-2 leading-7">
                  <template
                    v-for="(number, index) in phoneNumbers(entry.phone)"
                    :key="number"
                  >
                    <span v-if="index"> / </span>
                    <a
                      :href="telephoneHref(number)"
                      class="font-medium text-primary underline-offset-4 hover:underline"
                      :aria-label="`Call ${entry.office} at ${number}`"
                    >
                      {{ number }}
                    </a>
                  </template>
                </p>
              </div>
            </div>
          </UCard>
        </UPageGrid>
      </section>

      <div class="space-y-7">
        <section
          v-for="group in groups"
          :key="group"
          :aria-labelledby="`directory-${group.replaceAll(' ', '-')}`"
        >
          <h2
            :id="`directory-${group.replaceAll(' ', '-')}`"
            class="mb-3 font-domine text-xl font-semibold text-highlighted"
          >
            {{ group }}
          </h2>
          <div
            class="max-h-144 overflow-auto rounded-lg border border-default bg-default"
          >
            <table class="w-full min-w-[32rem] text-left">
              <thead
                class="sticky top-0 z-10 bg-default/75 text-muted backdrop-blur-sm"
              >
                <tr>
                  <th
                    scope="col"
                    class="whitespace-nowrap px-4 py-3 font-semibold text-muted"
                  >
                    Office
                  </th>
                  <th
                    scope="col"
                    class="whitespace-nowrap px-4 py-3 font-semibold text-muted"
                  >
                    Telephone
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-default">
                <tr
                  v-for="entry in municipalOfficeDirectory.filter(
                    (item) => item.group === group,
                  )"
                  :key="entry.office"
                >
                  <th scope="row" class="px-4 py-3 font-medium text-muted">
                    <UTooltip
                      :text="entry.office"
                      :ui="{
                        content: 'h-auto max-w-[min(32rem,calc(100vw-2rem))] items-start',
                        text: 'whitespace-normal break-words text-sm',
                      }"
                    >
                      <span
                        tabindex="0"
                        class="block max-w-[calc(100vw-6rem)] truncate rounded-sm focus-visible:outline-2 focus-visible:outline-primary sm:max-w-[32rem]"
                      >
                        {{ entry.office }}
                      </span>
                    </UTooltip>
                  </th>
                  <td class="px-4 py-3 text-muted">
                    <template
                      v-for="(number, index) in phoneNumbers(entry.phone)"
                      :key="number"
                    >
                      <span v-if="index"> / </span>
                      <a
                        :href="telephoneHref(number)"
                        class="whitespace-nowrap text-primary underline-offset-4 hover:underline"
                      >
                        {{ number }}
                      </a>
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>

      <p class="mt-7 text-sm leading-6 text-muted">
        This list preserves the legacy hotlines, which may have changed. For the
        official office list and full service procedures, see the
        <a
          :href="citizensCharter.source"
          target="_blank"
          rel="noopener"
          class="text-primary underline-offset-4 hover:underline"
        >
          2026 Citizen's Charter </a
        >.
      </p>
    </UContainer>
  </section>
</template>
