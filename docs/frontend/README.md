# Frontend

Nuxt 4 and Vue 3 site using Nuxt UI, TypeScript, Tailwind CSS, and Pinia.

## Structure

- `frontend/app/pages/` — file-based public and staff routes; see [Site routes](../site-routes.md).
- `frontend/app/components/lgu/` — page sections, shared archives, and content details.
- `frontend/app/layouts/` — global page layout and the transparency category layout.
- `frontend/app/composables/` — public-content access and authentication helpers.
- `frontend/app/utils/` — municipal information, service links, and local public content.

`app.vue` renders the global utility bar, header, main route outlet, and footer. The homepage composes its sections from `components/lgu`; archive/detail routes reuse `PublicContentArchive` and `PublicContentDetail`.

## Data boundary

Public pages currently use the local content module. The staff CMS uses authenticated backend API requests. See [Public content logic](../business-logic/public-content.md) for the route mapping and boundary.
