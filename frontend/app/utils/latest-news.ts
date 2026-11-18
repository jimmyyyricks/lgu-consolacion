import type { PublicContentItem } from '~/composables/usePublicContent'

export const latestNewsSlides = (
  published: PublicContentItem[],
  fallback: PublicContentItem[],
  limit = 5
) => {
  const bySlug = new Map<string, PublicContentItem>()
  for (const item of [...published, ...fallback]) {
    if (!bySlug.has(item.slug)) bySlug.set(item.slug, item)
  }

  return [...bySlug.values()]
    .sort((a, b) => {
      const aDate = Date.parse(a.record_date || a.published_at || a.created_at)
      const bDate = Date.parse(b.record_date || b.published_at || b.created_at)
      return bDate - aDate
    })
    .slice(0, limit)
}
