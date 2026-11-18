<script setup lang="ts">
import type {
  PublicContentItem,
  PublicContentKind
} from '~/composables/usePublicContent'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ middleware: 'auth' })

const config = useRuntimeConfig()
const authStore = useAuthStore()
const toast = useToast()
const apiUrl = String(config.public.apiUrl || '/api').replace(/\/$/, '')
const kinds: PublicContentKind[] = [
  'ordinance',
  'resolution',
  'memorandum',
  'executive_order',
  'disclosure',
  'bid',
  'form',
  'government_action',
  'news',
  'tourism'
]
const documentKinds = new Set<PublicContentKind>([
  'ordinance',
  'resolution',
  'memorandum',
  'executive_order',
  'disclosure',
  'bid',
  'form'
])

const records = ref<PublicContentItem[]>([])
const loading = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const editingSlug = ref<string | null>(null)
const state = reactive({
  kind: 'ordinance' as PublicContentKind,
  title: '',
  document_number: '',
  summary: '',
  body: '',
  category: '',
  image_url: '',
  featured: false,
  record_date: '',
  drive_url: ''
})

const headers = computed(() => ({
  Authorization: `Bearer ${authStore.token || ''}`
}))

function getErrorDetail(error: unknown) {
  if (
    typeof error === 'object'
    && error !== null
    && 'data' in error
    && typeof error.data === 'object'
    && error.data !== null
    && 'detail' in error.data
    && typeof error.data.detail === 'string'
  ) {
    return error.data.detail
  }
  return null
}

async function loadRecords() {
  loading.value = true
  errorMessage.value = ''
  try {
    records.value = await $fetch<PublicContentItem[]>(`${apiUrl}/content/admin/all`, {
      headers: headers.value
    })
  } catch (error: unknown) {
    errorMessage.value
      = getErrorDetail(error) || 'Could not load content. Check your staff access.'
  } finally {
    loading.value = false
  }
}

function clearForm() {
  editingSlug.value = null
  Object.assign(state, {
    kind: 'ordinance',
    title: '',
    document_number: '',
    summary: '',
    body: '',
    category: '',
    image_url: '',
    featured: false,
    record_date: '',
    drive_url: ''
  })
}

function editRecord(item: PublicContentItem) {
  editingSlug.value = item.slug
  Object.assign(state, {
    kind: item.kind,
    title: item.title,
    document_number: item.document_number || '',
    summary: item.summary,
    body: item.body || '',
    category: item.category || '',
    image_url: item.image_url || '',
    featured: item.featured,
    record_date: item.record_date || '',
    drive_url: item.drive_file_id
      ? `https://drive.google.com/file/d/${item.drive_file_id}/view`
      : ''
  })
}

async function save(status: 'draft' | 'published' = 'draft') {
  saving.value = true
  errorMessage.value = ''
  const payload = {
    ...state,
    status,
    document_number: state.document_number || null,
    category: state.category || null,
    image_url: state.image_url || null,
    summary: state.summary || undefined,
    featured: state.featured,
    record_date: state.record_date || null,
    body: state.body || null,
    drive_url: state.drive_url || null
  }

  try {
    if (editingSlug.value) {
      await $fetch(`${apiUrl}/content/${encodeURIComponent(editingSlug.value)}`, {
        method: 'PATCH',
        headers: headers.value,
        body: payload
      })
    } else {
      const slugBase = state.title
        .normalize('NFKD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '')
      const slugPrefix = slugBase.slice(0, 160).replace(/-+$/g, '') || state.kind.replaceAll('_', '-')
      const slug = `${slugPrefix}-${Date.now().toString(36)}`
      await $fetch(`${apiUrl}/content`, {
        method: 'POST',
        headers: headers.value,
        body: { ...payload, slug, kind: state.kind }
      })
    }
    toast.add({
      title: status === 'published' ? 'Content published' : 'Draft saved',
      color: 'success'
    })
    clearForm()
    await loadRecords()
  } catch (error: unknown) {
    errorMessage.value
      = getErrorDetail(error) || 'Could not save this record. Review the fields and try again.'
  } finally {
    saving.value = false
  }
}

onMounted(loadRecords)
</script>

<template>
  <div class="space-y-8">
    <header class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <p class="text-sm font-semibold uppercase tracking-normal text-primary">
          Staff workspace
        </p>
        <h1 class="mt-2 font-domine text-3xl font-semibold text-highlighted">
          Public content
        </h1>
        <p class="mt-2 max-w-2xl leading-7 text-toned">
          Prepare verified news, government actions, tourism information, and public records.
        </p>
      </div>
      <UButton
        v-if="editingSlug"
        color="neutral"
        variant="outline"
        size="lg"
        @click="clearForm"
      >
        New record
      </UButton>
    </header>

    <UAlert
      v-if="errorMessage"
      color="error"
      variant="subtle"
      title="Content could not be saved or loaded"
      :description="String(errorMessage)"
    />

    <UCard>
      <template #header>
        <h2 class="font-domine text-xl font-semibold text-highlighted">
          {{ editingSlug ? "Edit record" : "Create a record" }}
        </h2>
      </template>

      <UForm
        :state="state"
        class="grid gap-4 sm:grid-cols-2"
        @submit="save()"
      >
        <UFormField
          label="Content type"
          name="kind"
          size="lg"
          required
        >
          <USelect
            v-model="state.kind"
            :items="kinds"
            size="lg"
            class="w-full"
          />
        </UFormField>
        <UFormField
          label="Title"
          name="title"
          size="lg"
          required
          class="sm:col-span-2"
        >
          <UInput
            v-model="state.title"
            maxlength="300"
            size="lg"
            class="w-full"
          />
        </UFormField>
        <UFormField
          label="Document number"
          name="document_number"
          size="lg"
        >
          <UInput
            v-model="state.document_number"
            size="lg"
            class="w-full"
          />
        </UFormField>
        <UFormField
          label="Category"
          name="category"
          size="lg"
        >
          <UInput
            v-model="state.category"
            size="lg"
            class="w-full"
          />
        </UFormField>
        <UFormField
          label="Record date"
          name="record_date"
          size="lg"
        >
          <UInput
            v-model="state.record_date"
            type="date"
            size="lg"
            class="w-full"
          />
        </UFormField>
        <UFormField
          label="Story image"
          name="image_url"
          size="lg"
          description="Use a local path such as /images/story.jpg or a secure HTTPS image URL."
          class="sm:col-span-2"
        >
          <UInput
            v-model="state.image_url"
            type="text"
            placeholder="/images/story.jpg"
            size="lg"
            class="w-full"
          />
          <img
            v-if="state.image_url"
            :src="state.image_url"
            alt="Story image preview"
            class="mt-3 max-h-48 w-full rounded-md border border-default object-cover"
          >
        </UFormField>
        <UFormField
          v-if="state.kind === 'news'"
          name="featured"
          size="lg"
          class="sm:col-span-2"
        >
          <UCheckbox
            v-model="state.featured"
            size="lg"
            label="Feature this news or event on the homepage"
          />
        </UFormField>
        <UFormField
          label="Public Google Drive PDF link"
          name="drive_url"
          size="lg"
        >
          <UInput
            v-model="state.drive_url"
            type="url"
            placeholder="https://drive.google.com/file/d/…/view"
            size="lg"
            class="w-full"
          />
        </UFormField>
        <UFormField
          v-if="!documentKinds.has(state.kind)"
          label="Summary"
          name="summary"
          size="lg"
          required
          class="sm:col-span-2"
        >
          <UTextarea
            v-model="state.summary"
            :rows="3"
            maxlength="4000"
            size="lg"
            class="w-full"
          />
        </UFormField>
        <UFormField
          label="Additional text"
          name="body"
          size="lg"
          class="sm:col-span-2"
        >
          <UTextarea
            v-model="state.body"
            :rows="7"
            size="lg"
            class="w-full"
          />
        </UFormField>

        <div class="flex flex-wrap gap-3 sm:col-span-2">
          <UButton
            type="submit"
            size="lg"
            :loading="saving"
          >
            Save draft
          </UButton>
          <UButton
            type="button"
            color="secondary"
            size="lg"
            :loading="saving"
            @click="save('published')"
          >
            Publish
          </UButton>
        </div>
      </UForm>

      <p class="mt-4 text-sm text-muted">
        Published PDFs must be shared for anyone with the link to view. Verify the
        PDF in a signed-out browser before publishing. The PDF viewer has an
        external Google Drive fallback.
      </p>
    </UCard>

    <section aria-labelledby="content-records-heading">
      <div class="mb-4 flex items-center justify-between gap-3">
        <h2
          id="content-records-heading"
          class="font-domine text-2xl font-semibold text-highlighted"
        >
          Existing records
        </h2>
        <UButton
          icon="i-lucide-refresh-cw"
          color="neutral"
          variant="ghost"
          size="lg"
          :loading="loading"
          aria-label="Refresh records"
          @click="loadRecords"
        />
      </div>
      <UAlert
        v-if="!loading && !records.length && !errorMessage"
        color="neutral"
        variant="subtle"
        title="No content has been added yet"
        description="Create a draft above. Drafts are not visible on the public website."
      />
      <div
        v-else
        class="divide-y divide-default border-y border-default"
      >
        <article
          v-for="item in records"
          :key="item.id"
          class="flex flex-wrap items-center justify-between gap-4 py-4"
        >
          <div class="min-w-0">
            <p class="text-xs uppercase tracking-wide text-muted">
              {{ item.kind.replaceAll("_", " ") }} · {{ item.status }}<span v-if="item.featured"> · featured</span>
            </p>
            <h3 class="mt-1 font-medium text-highlighted">
              {{ item.title }}
            </h3>
            <p
              v-if="item.summary"
              class="mt-1 line-clamp-2 text-sm text-toned"
            >
              {{ item.summary }}
            </p>
          </div>
          <UButton
            color="neutral"
            variant="outline"
            icon="i-lucide-pencil"
            size="lg"
            @click="editRecord(item)"
          >
            Edit
          </UButton>
        </article>
      </div>
    </section>
  </div>
</template>
