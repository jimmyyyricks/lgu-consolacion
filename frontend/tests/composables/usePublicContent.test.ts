import {
  publicContentDate,
  publicContentPath,
  usePublicContent,
  usePublicContentArchive,
  type PublicContentItem
} from '~/composables/usePublicContent'
import { getStaticPublicContent } from '~/utils/static-public-content'
import { ref } from 'vue'

const item = (kind: PublicContentItem['kind']): PublicContentItem =>
  ({
    kind,
    slug: 'record-2026'
  }) as PublicContentItem

describe('public content routes', () => {
  it('uses the news and tourism detail routes', () => {
    expect(publicContentPath(item('news'))).toBe('/news/record-2026')
    expect(publicContentPath(item('tourism'))).toBe('/tourism/record-2026')
  })

  it('uses the government actions detail route', () => {
    expect(publicContentPath(item('government_action'))).toBe(
      '/about/actions/record-2026'
    )
  })

  it('routes document kinds to the transparency detail page', () => {
    expect(publicContentPath(item('ordinance'))).toBe(
      '/transparency/document/record-2026?kind=ordinance'
    )
    expect(publicContentPath(item('memorandum'))).toBe(
      '/transparency/document/record-2026?kind=memorandum'
    )
  })
})

describe('public content dates', () => {
  it('formats an ISO date consistently', () => {
    expect(publicContentDate('2026-01-02')).toBe('January 2, 2026')
  })

  it('returns null when no date is available', () => {
    expect(publicContentDate(null)).toBeNull()
  })
})

describe('static public content', () => {
  it('provides verified legacy news, tourism, ordinances, resolutions, and forms', () => {
    const kinds = new Set(getStaticPublicContent().map(item => item.kind))
    expect(kinds).toEqual(
      new Set(['news', 'government_action', 'tourism', 'ordinance', 'resolution', 'form', 'bid'])
    )
  })

  it('includes actual ordinance titles without attaching unprovided files', () => {
    const ordinances = getStaticPublicContent('ordinance')
    expect(ordinances.map(item => item.title)).toContain(
      'PROVIDING A COMPREHENSIVE YOUTH WELFARE & DEV\'T. CODE OF MUN. GOV\'T.'
    )
    expect(ordinances.every(item => item.drive_file_id === null)).toBe(true)
  })

  it('filters static content by search, year, and pagination', () => {
    const search = ref('youth welfare')
    const year = ref(2024 as number | undefined)
    const offset = ref(0)
    const ordinances = usePublicContent({ kind: 'ordinance', search, year, offset })

    expect(ordinances.data.value).toHaveLength(1)
    expect(ordinances.data.value[0]?.slug).toBe('ordinance-35-2024')
  })

  it('filters and pages the static archive without an API response', async () => {
    const archive = await usePublicContentArchive({
      kind: 'resolution',
      search: ref('Resolution No. 99'),
      year: ref(undefined),
      offset: ref(0),
      limit: ref(10)
    })

    expect(archive.total.value).toBe(1)
    expect(archive.data.value[0]?.slug).toBe('resolution-99-2024')
  })
})
