<script setup lang="ts">
import {
  citizensCharter,
  municipalInformation,
} from "~/utils/municipal-information";
</script>

<template>
  <section
    id="citizens-charter"
    aria-labelledby="citizens-charter-heading"
    class="scroll-mt-32 bg-muted/40"
  >
    <UContainer class="py-8 sm:py-10 lg:py-12">
      <div class="mb-7 max-w-3xl">
        <h2
          id="citizens-charter-heading"
          class="font-domine text-3xl font-semibold text-highlighted sm:text-4xl"
        >
          Citizen's Charter
        </h2>
        <p class="mt-3 leading-7 text-toned">
          {{ citizensCharter.edition }}. The Municipality's official service
          commitments and a summary of its office services.
        </p>
      </div>

      <UPageGrid class="gap-4 sm:grid-cols-1 lg:grid-cols-2">
        <UCard variant="outline">
          <h3 class="font-domine text-2xl font-semibold text-highlighted">
            Development Goal
          </h3>
          <p class="mt-3 leading-7 text-toned">
            {{ municipalInformation.developmentGoal }}
          </p>
          <p class="mt-3 leading-7 text-toned">
            {{ municipalInformation.developmentObjectives }}
          </p>
          <p class="mt-3 text-sm leading-6 text-muted">
            From the Comprehensive Land Use Plan 2024–2033.
          </p>
        </UCard>

        <UCard variant="outline">
          <h3 class="font-domine text-2xl font-semibold text-highlighted">
            Service Pledge
          </h3>
          <p class="mt-3 leading-7 text-toned">
            {{ citizensCharter.servicePledgeIntro }}
          </p>
          <ul class="mt-5 divide-y divide-default">
            <li
              v-for="pledge in citizensCharter.servicePledge"
              :key="pledge"
              class="flex gap-3 py-4 leading-7 text-toned first:pt-0"
            >
              <UIcon
                name="i-lucide-check"
                class="mt-1 size-5 shrink-0 text-success"
              />
              <span>{{ pledge }}</span>
            </li>
          </ul>
        </UCard>
      </UPageGrid>

      <UPageGrid class="mt-4 gap-4 lg:grid-cols-2">
        <UCard variant="outline">
          <h3 class="font-domine text-xl font-semibold text-highlighted">
            Visit or Contact the Municipal Hall
          </h3>
          <dl class="mt-4 space-y-3 leading-7">
            <div>
              <dt class="font-medium text-highlighted">Office Hours</dt>
              <dd class="text-toned">
                {{ municipalInformation.officeHours }}
              </dd>
            </div>
            <div>
              <dt class="font-medium text-highlighted">Telephone</dt>
              <dd>
                <a
                  class="text-primary underline-offset-4 hover:underline"
                  href="tel:+63322392908"
                >
                  {{ municipalInformation.phone }}
                </a>
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
          <p class="mt-4 text-sm leading-6 text-muted">
            Confirm schedules with the relevant office before visiting, as hours
            may change for holidays or advisories.
          </p>
        </UCard>

        <UCard
          variant="outline"
          :ui="{ body: 'flex h-full flex-col items-start' }"
        >
          <h3 class="font-domine text-xl font-semibold text-highlighted">
            Services Across Municipal Offices
          </h3>
          <p class="mt-3 flex-1 leading-7 text-toned">
            {{ citizensCharter.otherServicesSummary }}
          </p>
          <UButton
            :to="citizensCharter.source"
            target="_blank"
            rel="noopener"
            trailing-icon="i-lucide-arrow-up-right"
            size="lg"
            class="mt-5"
          >
            View the Full Charter
          </UButton>
        </UCard>
      </UPageGrid>

      <UCard variant="outline" class="mt-4">
        <h3 class="font-domine text-xl font-semibold text-highlighted">
          Feedback and Complaints
        </h3>
        <div class="mt-4 grid gap-5 leading-7 text-toned lg:grid-cols-3">
          <div>
            <h4 class="font-semibold text-highlighted">
              Submit Feedback or a Complaint
            </h4>
            <p class="mt-2">
              {{ citizensCharter.feedback.dropBox }}
            </p>
            <p class="mt-2">
              {{ citizensCharter.feedback.complaintSubmission }}
            </p>
            <p class="mt-2">
              Contact Center ng Bayan:
              <a
                class="text-primary underline-offset-4 hover:underline"
                href="tel:+63322392908"
              >
                {{ citizensCharter.feedback.telephone }}
              </a>
            </p>
          </div>
          <div>
            <h4 class="font-semibold text-highlighted">Feedback Process</h4>
            <p class="mt-2">
              {{ citizensCharter.feedback.feedbackProcess }}
            </p>
          </div>
          <div>
            <h4 class="font-semibold text-highlighted">Complaint Process</h4>
            <p class="mt-2">
              {{ citizensCharter.feedback.complaintProcess }}
            </p>
          </div>
        </div>
      </UCard>
    </UContainer>
  </section>
</template>
