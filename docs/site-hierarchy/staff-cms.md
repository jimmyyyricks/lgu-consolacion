# Staff Sign-in and CMS

## Route flow

1. Header or footer **Staff sign in** opens `/login`.
2. Successful authentication sends the user to `/admin/content`.
3. `/admin` provides the authenticated workspace shell.
4. `/admin/`, `/admin/permissions`, and `/admin/roles` redirect to `/admin/content`.

Admin pages use the `auth` middleware. Unauthenticated visitors are redirected to `/login`.

## Public content workspace

`/admin/content` creates and edits ordinances, resolutions, memoranda, executive orders, disclosures, bids, forms, government actions, news, and tourism entries. Editors can save drafts or publish records.

The CMS uses authenticated API requests. Public route mappings are listed in [Site routes](../site-routes.md); the current separation between CMS data and public page data is in [Business logic](../business-logic/public-content.md).
