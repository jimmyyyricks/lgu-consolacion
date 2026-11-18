# Public Content

The site presents five public content groups: transparency records, government actions, news, tourism, and downloadable forms.

## Content kinds and pages

CMS kinds map to public pages as follows:

| Kind | Public route |
| --- | --- |
| `ordinance`, `resolution`, `executive_order`, `memorandum`, `disclosure`, `bid`, `form` | `/transparency/<archive>` and `/transparency/document/:slug?kind=...` |
| `government_action` | `/about/actions` and `/about/actions/:slug` |
| `news` | `/news` and `/news/:slug` |
| `tourism` | `/tourism` and `/tourism/:slug` |

Content records may include a title, summary, body, category, date, image, document number, featured flag, publication status, and Drive file reference.

## Current data flow

- Public Vue pages currently read local records from `frontend/app/utils/static-public-content.ts` through `usePublicContent`.
- The backend exposes published-content endpoints under `/api/content`, including list, archive, and slug lookup.
- The staff CMS uses authenticated API requests to load all records, create records, and update records.
- These paths are not currently connected in the frontend: publishing in the CMS does not update the local records used by public pages.
- Drafts are intended for staff preparation and are not shown in public archive views.

This boundary is the main constraint when tracing content from [the CMS](../site-hierarchy/staff-cms.md) to [public pages](../site-routes.md).
