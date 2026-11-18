<script setup lang="ts">
import { watchDebounced } from "@vueuse/core";
import type { TableColumn } from "@nuxt/ui";
import type {
  PublicContentItem,
  PublicContentKind,
} from "~/composables/usePublicContent";

const documentKinds = new Set<PublicContentKind>([
  "ordinance",
  "resolution",
  "memorandum",
  "executive_order",
  "disclosure",
  "bid",
  "form",
]);

const props = defineProps<{
  kind: PublicContentKind;
  title: string;
  description: string;
}>();

const searchInput = ref("");
const search = ref("");
const selectedYear = ref(0);
const year = computed(() => selectedYear.value || undefined);
const page = ref(1);
const pageSize = ref(20);
const offset = ref(0);
const selectedRecord = ref<PublicContentItem | null>(null);
const previewOpen = ref(false);
const { data, total, years, error, pending } = await usePublicContentArchive({
  kind: props.kind,
  search,
  year,
  offset,
  limit: pageSize,
  recordsOnly: documentKinds.has(props.kind),
});

const columns: TableColumn<PublicContentItem>[] = [
  {
    accessorKey: "record_date",
    header: "Record Date",
    meta: { class: { th: "hidden sm:table-cell", td: "hidden sm:table-cell" } },
  },
  { accessorKey: "title", header: "Title" },
  {
    accessorKey: "category",
    header: "Category",
    meta: { class: { th: "hidden sm:table-cell", td: "hidden sm:table-cell" } },
  },
  {
    accessorKey: "document_number",
    header: "Document #",
    meta: { class: { th: "hidden sm:table-cell", td: "hidden sm:table-cell" } },
  },
];
const yearOptions = computed(() => [
  { label: "All years", value: 0 },
  ...years.value.map((value) => ({ label: String(value), value })),
]);
const pageSizeOptions = [10, 20, 50].map((value) => ({
  label: `${value} per page`,
  value,
}));
const pageCount = computed(() => Math.ceil(total.value / pageSize.value));
const emptyMessage = computed(() =>
  search.value || year.value
    ? "No records match these filters."
    : "No migrated records are listed here yet.",
);

function handleRecordClick(event: Event, item: PublicContentItem) {
  if (
    event instanceof MouseEvent &&
    (event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey)
  ) {
    return;
  }
  event.preventDefault();
  if (!documentKinds.has(item.kind)) {
    void navigateTo(publicContentPath(item));
    return;
  }
  selectedRecord.value = item;
  previewOpen.value = true;
}

function handleRowSelect(event: Event, row: { original: PublicContentItem }) {
  handleRecordClick(event, row.original);
}

watchDebounced(
  searchInput,
  (value) => {
    search.value = value;
  },
  { debounce: 300, maxWait: 1000 },
);
watch([searchInput, selectedYear, pageSize], () => {
  page.value = 1;
});
watch([page, pageSize], () => {
  offset.value = (page.value - 1) * pageSize.value;
});

useSeoMeta({
  title: () => `${props.title} | Municipality of Consolacion`,
  description: () => props.description,
  ogTitle: () => `${props.title} | Municipality of Consolacion`,
  ogDescription: () => props.description,
});
</script>

<template>
  <UPage>
    <UPageHeader
      :title="title"
      :description="description"
      :ui="{
        title: 'font-domine text-3xl font-semibold sm:text-4xl',
        container: 'mx-auto w-full max-w-(--ui-container) px-4 sm:px-6 lg:px-8',
      }"
    >
      <template #links>
        <div class="flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
          <UInput
            v-model="searchInput"
            icon="i-lucide-search"
            placeholder="Search records"
            aria-label="Search public records"
            size="lg"
            class="w-full sm:w-72"
          />
          <USelectMenu
            v-model="selectedYear"
            :items="yearOptions"
            value-key="value"
            aria-label="Filter by publication year"
            placeholder="All years"
            size="lg"
            class="w-full sm:w-32"
          />
        </div>
      </template>
    </UPageHeader>

    <UPageBody>
      <UContainer class="pt-2">
        <UAlert
          v-if="documentKinds.has(kind)"
          class="mb-5"
          color="neutral"
          variant="subtle"
          title="Static title index"
          description="These entries contain titles transcribed from the legacy site. Original documents are not attached; contact the Sangguniang Bayan Office for official copies."
        />
        <UAlert
          v-if="error"
          color="error"
          variant="subtle"
          title="Records are temporarily unavailable"
          description="Please try again later."
        />
        <UTable
          v-else
          :data="data"
          :columns="columns"
          :loading="pending"
          :empty="emptyMessage"
          :pagination-options="{ manualPagination: true, pageCount }"
          :on-select="handleRowSelect"
          sticky="header"
          :ui="{
            tr: '[&[data-selectable=true]]:cursor-pointer',
            th: 'whitespace-nowrap py-6 font-bold text-muted',
            root: 'max-h-144 border rounded-sm border-gray-200 dark:border-gray-800',
          }"
        >
          <template #title-cell="{ row }">
            <div>
              <UTooltip
                :text="row.original.title"
                :ui="{
                  content: 'h-auto max-w-[min(32rem,calc(100vw-2rem))] items-start',
                  text: 'whitespace-normal break-words text-sm',
                }"
              >
                <a
                  :href="publicContentPath(row.original)"
                  :aria-haspopup="
                    documentKinds.has(row.original.kind) ? 'dialog' : undefined
                  "
                  class="block max-w-[calc(100vw-6rem)] truncate text-muted font-medium hover:text-primary focus-visible:outline-primary sm:max-w-[32rem]"
                  @click="handleRecordClick($event, row.original)"
                >
                  {{ row.original.title }}
                </a>
              </UTooltip>
              <div
                class="mt-1 flex flex-wrap gap-x-3 gap-y-1 text-sm text-muted sm:hidden"
              >
                <span v-if="row.original.document_number">
                  {{ row.original.document_number }}
                </span>
                <span v-if="row.original.category">
                  {{ row.original.category }}
                </span>
                <time
                  v-if="publicContentDate(row.original.record_date)"
                  :datetime="row.original.record_date || undefined"
                >
                  {{ publicContentDate(row.original.record_date) }}
                </time>
              </div>
            </div>
          </template>
          <template #record_date-cell="{ row }">
            {{ publicContentDate(row.original.record_date) || "—" }}
          </template>
        </UTable>

        <div
          v-if="!error && total"
          class="flex flex-col gap-4 pt-4 sm:flex-row sm:items-center sm:justify-between"
        >
          <p class="text-sm text-toned">
            Showing {{ offset + 1 }}–{{
              Math.min(offset + data.length, total)
            }}
            of {{ total }} records
          </p>
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
            <USelectMenu
              v-model="pageSize"
              :items="pageSizeOptions"
              value-key="value"
              :search-input="false"
              aria-label="Records per page"
              size="lg"
              class="w-full sm:w-36"
            />
            <UPagination
              v-model:page="page"
              :total="total"
              :items-per-page="pageSize"
              :disabled="pending"
              aria-label="Public record pages"
            />
          </div>
        </div>
        <UModal
          v-model:open="previewOpen"
          :title="selectedRecord?.title || 'Public record'"
          :description="selectedRecord?.summary || undefined"
          :ui="{
            content: 'w-[calc(100vw-2rem)] max-w-5xl',
            body: 'p-0',
          }"
        >
          <template #body>
            <div class="">
              <LguDrivePdfPreview
                v-if="selectedRecord?.drive_file_id"
                :file-id="selectedRecord.drive_file_id"
                :title="selectedRecord.title"
              />
              <UAlert
                v-else
                color="neutral"
                variant="subtle"
                title="PDF preview unavailable"
                description="This record does not have a Google Drive file attached."
              />
            </div>
          </template>
        </UModal>
      </UContainer>
    </UPageBody>
  </UPage>
</template>
