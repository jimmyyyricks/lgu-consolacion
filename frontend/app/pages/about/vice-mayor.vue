<script setup lang="ts">
import { citizensCharter, municipalInformation, municipalOfficeDirectory } from '~/utils/municipal-information'
import { titleCaseLabel } from '~/utils/title-case'

definePageMeta({ layout: 'about' })

const office = municipalOfficeDirectory.find(item => item.office === 'Vice Mayor\'s Office')

useSeoMeta({
  title: 'Office of the Vice Mayor | Municipality of Consolacion',
  description: 'Read the Vice Mayor\'s message, find office contacts, and review Sangguniang Bayan Charter services.'
})
</script>

<template>
  <UPage>
    <UPageHeader
      title="Office of the Vice Mayor"
      description="A message from the Vice Mayor, office contact details, and Sangguniang Bayan Charter services."
      :ui="{
        title: 'font-domine text-3xl font-semibold sm:text-4xl',
        container: 'mx-auto w-full max-w-(--ui-container) px-4 sm:px-6 lg:px-8',
      }"
    />
    <UPageBody>
      <UContainer class="py-8 sm:py-12">
        <UCard v-if="office" variant="outline" class="mb-8 max-w-2xl">
          <h2 class="font-domine text-xl font-semibold text-highlighted">
            Office Contact
          </h2>
          <dl class="mt-4 grid gap-4 sm:grid-cols-3">
            <div>
              <dt class="font-medium text-highlighted">Location</dt>
              <dd class="mt-1 text-toned">
                Municipal Hall, {{ titleCaseLabel(office.group) }}
              </dd>
            </div>
            <div>
              <dt class="font-medium text-highlighted">Telephone</dt>
              <dd class="mt-1 text-toned">
                {{ office.phone }}
              </dd>
            </div>
            <div>
              <dt class="font-medium text-highlighted">Office Hours</dt>
              <dd class="mt-1 text-toned">
                {{ municipalInformation.officeHours }}
              </dd>
            </div>
          </dl>
          <UButton
            to="/about/office-directory"
            size="lg"
            trailing-icon="i-lucide-arrow-right"
            class="mt-6"
          >
            View Office Directory
          </UButton>
        </UCard>
      </UContainer>
      <LguMayorsDesk />
      <LguSection
        id="vice-mayor-charter-services"
        title="Citizen's Charter Services"
        description="The 2026 Charter groups these external services under the Office of the Municipal Vice-Mayor and the Sangguniang Bayan."
      >
        <template #actions>
          <UButton
            :to="citizensCharter.source"
            target="_blank"
            rel="noopener"
            variant="link"
            size="lg"
            trailing-icon="i-lucide-arrow-up-right"
          >
            Full Procedures
          </UButton>
        </template>
        <ul class="grid gap-3 sm:grid-cols-2">
          <li
            v-for="service in citizensCharter.viceMayorServices"
            :key="service"
            class="border-l-2 border-primary bg-muted/40 p-4 leading-7 text-default"
          >
            {{ service }}
          </li>
        </ul>
      </LguSection>
    </UPageBody>
  </UPage>
</template>
