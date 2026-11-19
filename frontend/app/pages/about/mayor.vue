<script setup lang="ts">
import { citizensCharter, municipalInformation, municipalOfficeDirectory } from '~/utils/municipal-information'
import { titleCaseLabel } from '~/utils/title-case'

definePageMeta({ layout: 'about' })

const office = municipalOfficeDirectory.find(item => item.office === 'Mayor\'s Office')

useSeoMeta({
  title: 'Office of the Mayor | Municipality of Consolacion',
  description: 'Contact details and Citizen\'s Charter services from the Mayor\'s Office of Consolacion.'
})
</script>

<template>
  <UPage>
    <UPageHeader
      title="Office of the Mayor"
      description="Municipal Hall contact details and Citizen's Charter services."
      :ui="{
        title: 'font-domine text-3xl font-semibold sm:text-4xl',
        container: 'mx-auto w-full max-w-(--ui-container) px-4 sm:px-6 lg:px-8',
      }"
    />
    <UPageBody>
      <UContainer class="py-8 sm:py-12">
        <UCard v-if="office" variant="outline" class="max-w-2xl">
          <h2 class="font-domine text-xl font-semibold text-highlighted">
            Office Contact
          </h2>
          <dl class="mt-4 space-y-3 leading-7">
            <div>
              <dt class="font-medium text-highlighted">Location</dt>
              <dd class="text-toned">Municipal Hall, {{ titleCaseLabel(office.group) }}</dd>
            </div>
            <div>
              <dt class="font-medium text-highlighted">Telephone</dt>
              <dd class="text-toned">
                {{ office.phone }}
              </dd>
            </div>
            <div>
              <dt class="font-medium text-highlighted">Office Hours</dt>
              <dd class="text-toned">
                {{ municipalInformation.officeHours }}
              </dd>
            </div>
            <div>
              <dt class="font-medium text-highlighted">Email</dt>
              <dd>
                <a
                  class="text-primary underline-offset-4 hover:underline"
                  :href="`mailto:${municipalInformation.email}`"
                >
                  {{ municipalInformation.email }}
                </a>
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
      <LguSection
        id="mayor-charter-services"
        title="Citizen's Charter Services"
        description="The 2026 Charter lists these services under the Office of the Municipal Mayor."
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
            v-for="service in citizensCharter.mayorServices"
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
