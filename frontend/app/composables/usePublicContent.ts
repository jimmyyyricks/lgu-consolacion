import { computed, ref, type Ref } from 'vue'
import { getStaticPublicContent } from '~/utils/static-public-content'

export type PublicContentKind
  = | 'ordinance'
    | 'resolution'
    | 'memorandum'
    | 'executive_order'
    | 'disclosure'
    | 'bid'
    | 'form'
    | 'government_action'
    | 'news'
    | 'tourism'

export interface PublicContentItem {
  id: string
  slug: string
  kind: PublicContentKind
  title: string
  document_number: string | null
  summary: string
  body: string | null
  category: string | null
  image_url: string | null
  featured: boolean
  record_date: string | null
  status: 'draft' | 'published' | 'archived'
  drive_file_id: string | null
  created_at: string
  updated_at: string
  published_at: string | null
}

export interface PublicContentArchivePage {
  items: PublicContentItem[]
  total: number
  years: number[]
}

const contentYear = (item: PublicContentItem) => {
  const publishedYear = item.published_at?.slice(0, 4)
  const documentYear = item.document_number?.match(/\b(19|20)\d{2}\b/)?.[0]
  const year = publishedYear || documentYear
  return year ? Number(year) : undefined
}

export const usePublicContent = (
  query: {
    kind?: PublicContentKind
    search?: Ref<string>
    year?: Ref<number | undefined>
    offset?: Ref<number>
    limit?: number
    recordsOnly?: boolean
  } = {}
) => {
  const data = computed(() => {
    const items = getStaticPublicContent(query.kind).filter(
      item => !query.recordsOnly || (item.kind !== 'news' && item.kind !== 'tourism')
    )
    const searchTerm = query.search?.value.trim().toLowerCase()
    return items
      .filter((item) => {
        const matchesSearch = !searchTerm
          || `${item.title} ${item.summary} ${item.category || ''}`
            .toLowerCase()
            .includes(searchTerm)
        const matchesYear = !query.year?.value
          || contentYear(item) === query.year.value
        return matchesSearch && matchesYear
      })
      .slice(query.offset?.value ?? 0, (query.offset?.value ?? 0) + (query.limit ?? 50))
  })

  return {
    data,
    error: ref(null),
    pending: ref(false),
    usingStatic: ref(true)
  }
}

export const usePublicContentArchive = async (query: {
  kind: PublicContentKind
  search: Readonly<Ref<string>>
  year: Readonly<Ref<number | undefined>>
  offset: Readonly<Ref<number>>
  limit: Readonly<Ref<number>>
  recordsOnly?: boolean
}) => {
  const records = computed(() =>
    getStaticPublicContent(query.kind).filter(
      item => !query.recordsOnly || (item.kind !== 'news' && item.kind !== 'tourism')
    )
  )
  const matchingRecords = computed(() => {
    const searchTerm = query.search.value.trim().toLowerCase()
    return records.value.filter((item) => {
      const matchesSearch = !searchTerm
        || `${item.title} ${item.document_number || ''} ${item.summary} ${item.category || ''}`
          .toLowerCase()
          .includes(searchTerm)
      const matchesYear = !query.year.value || contentYear(item) === query.year.value
      return matchesSearch && matchesYear
    })
  })
  const data = computed(() =>
    matchingRecords.value.slice(
      query.offset.value,
      query.offset.value + query.limit.value
    )
  )
  const years = computed(() =>
    [...new Set(records.value.map(contentYear).filter((year): year is number => Boolean(year)))]
      .sort((a, b) => b - a)
  )

  return {
    data,
    total: computed(() => matchingRecords.value.length),
    years,
    error: ref(null),
    pending: ref(false),
    usingStatic: ref(true)
  }
}

export const publicContentPath = (item: PublicContentItem) => {
  if (item.kind === 'news') return `/news/${item.slug}`
  if (item.kind === 'tourism') return `/tourism/${item.slug}`
  if (item.kind === 'government_action') {
    return `/about/actions/${item.slug}`
  }
  return `/transparency/document/${item.slug}?kind=${item.kind}`
}

export const publicContentDate = (value: string | null) => {
  if (!value) return null
  return new Intl.DateTimeFormat('en-PH', {
    dateStyle: 'long',
    timeZone: 'UTC'
  }).format(new Date(`${value.slice(0, 10)}T00:00:00Z`))
}
