<script setup lang="ts">
import { getStaticPublicContentBySlug } from '~/utils/static-public-content'

const props = defineProps<{
  slug: string
  backTo?: string
}>()

const content = getStaticPublicContentBySlug(props.slug)

if (!content) {
  throw createError({ statusCode: 404, statusMessage: 'Record not found' })
}

const pageTitle = content.title

useSeoMeta({
  title: () => `${pageTitle} | Municipality of Consolacion`,
  description: () => content.summary,
  ogTitle: () => pageTitle,
  ogDescription: () => content.summary,
  robots: 'index, follow'
})
</script>

<template>
  <UPage>
    <UPageBody>
      <UContainer class="py-8 sm:py-12">
        <UButton
          :to="backTo || '/transparency'"
          variant="link"
          color="neutral"
          size="lg"
          icon="i-lucide-arrow-left"
          class="mb-6 px-0"
        >
          Back to record list
        </UButton>

        <article class="mx-auto max-w-4xl">
          <div class="flex flex-wrap gap-x-3 gap-y-1 text-sm text-muted">
            <span>{{ content.kind.replaceAll("_", " ") }}</span>
            <span v-if="content.document_number">{{ content.document_number }}</span>
            <span v-if="content.category">{{ content.category }}</span>
            <time
              v-if="publicContentDate(content.record_date)"
              :datetime="content.record_date || undefined"
            >
              {{ publicContentDate(content.record_date) }}
            </time>
          </div>
          <h1 class="mt-3 font-domine text-3xl font-semibold leading-tight text-highlighted sm:text-4xl">
            {{ content.title }}
          </h1>
          <p
            v-if="content.summary"
            class="mt-5 text-lg leading-8 text-toned"
          >
            {{ content.summary }}
          </p>
          <div
            v-if="content.body"
            class="prose prose-neutral mt-8 max-w-none whitespace-pre-line leading-8"
          >
            {{ content.body }}
          </div>
          <div
            v-if="content.drive_file_id"
            class="mt-10"
          >
            <h2 class="mb-4 font-domine text-2xl font-semibold text-highlighted">
              Official document
            </h2>
            <LguDrivePdfPreview
              :file-id="content.drive_file_id"
              :title="content.title"
            />
          </div>
        </article>
      </UContainer>
    </UPageBody>
  </UPage>
</template>
