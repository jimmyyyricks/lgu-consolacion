import type { PublicContentItem } from '~/composables/usePublicContent'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const apiUrl = String(config.public.apiUrl || '/api').replace(/\/$/, '')
  const origin = getRequestURL(event).origin
  const paths = ['/', '/transparency', '/government/actions', '/news', '/tourism']

  let offset = 0
  while (true) {
    const records = await $fetch<PublicContentItem[]>(`${apiUrl}/content`, {
      query: { limit: 100, offset }
    }).catch(() => null)
    if (!records?.length) break
    for (const record of records) {
      if (record.kind === 'news') paths.push(`/news/${encodeURIComponent(record.slug)}`)
      else if (record.kind === 'tourism') paths.push(`/tourism/${encodeURIComponent(record.slug)}`)
      else if (record.kind === 'government_action') {
        paths.push(`/government/actions/${encodeURIComponent(record.slug)}`)
      } else {
        paths.push(`/transparency/document/${encodeURIComponent(record.slug)}`)
      }
    }
    if (records.length < 100) break
    offset += records.length
  }

  setResponseHeader(event, 'content-type', 'application/xml; charset=utf-8')
  setResponseHeader(event, 'cache-control', 'public, max-age=300')
  return `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${[
    ...new Set(paths)
  ]
    .map(path => `<url><loc>${origin}${path}</loc></url>`)
    .join('')}</urlset>`
})
