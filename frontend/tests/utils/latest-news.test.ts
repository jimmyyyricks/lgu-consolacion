import { latestNewsSlides } from '~/utils/latest-news'
import type { PublicContentItem } from '~/composables/usePublicContent'

const makeItem = (
  slug: string,
  recordDate: string
): PublicContentItem => ({
  id: slug,
  slug,
  kind: 'news',
  title: slug,
  document_number: null,
  summary: '',
  body: null,
  category: null,
  image_url: null,
  featured: false,
  record_date: recordDate,
  status: 'published',
  drive_file_id: null,
  created_at: `${recordDate}T00:00:00`,
  updated_at: `${recordDate}T00:00:00`,
  published_at: `${recordDate}T00:00:00`
})

describe('latestNewsSlides', () => {
  it('returns the five newest items by record date', () => {
    const items = [
      makeItem('older', '2026-01-01'),
      makeItem('newest', '2026-05-01'),
      makeItem('middle', '2026-03-01'),
      makeItem('fourth', '2026-02-01'),
      makeItem('third', '2026-04-01'),
      makeItem('second', '2026-04-15')
    ]

    expect(latestNewsSlides(items, []).map(item => item.slug)).toEqual([
      'newest',
      'second',
      'third',
      'middle',
      'fourth'
    ])
  })

  it('deduplicates static entries by slug', () => {
    const published = [makeItem('same', '2026-01-01'), makeItem('older', '2025-12-01')]
    const duplicate = makeItem('same', '2025-11-01')

    expect(latestNewsSlides(published, [duplicate]).map(item => item.slug)).toEqual([
      'same',
      'older'
    ])
  })
})
