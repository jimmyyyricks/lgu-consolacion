# Site Routes

Route index for the public website and staff content workspace. Routes are file-based in `frontend/app/pages`.

## Public site

| Route                     | Purpose                                                                   | Page notes                                         |
| ------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------- |
| `/`                       | Landing page and site entry point.                                        | [Landing page](site-hierarchy/landing-page.md)     |
| `/about`                  | Citizen's Charter, municipal overview, programs, and service commitments. | [About Consolacion](site-hierarchy/about-page.md)  |
| `/about/mayor`            | Mayor's Office contact information.                                       | [About Consolacion](site-hierarchy/about-page.md)  |
| `/about/vice-mayor`       | Vice Mayor's message and office contact information.                      | [About Consolacion](site-hierarchy/about-page.md)  |
| `/about/officials`        | Elected Sangguniang Bayan members.                                        | [About Consolacion](site-hierarchy/about-page.md)  |
| `/about/office-directory` | Municipal office contacts and emergency/community hotlines.               | [About Consolacion](site-hierarchy/about-page.md)  |
| `/about/actions`          | Government notices and actions archive.                                   | [About Consolacion](site-hierarchy/about-page.md)  |
| `/about/actions/:slug`    | Government action detail.                                                 | [About Consolacion](site-hierarchy/about-page.md)  |
| `/news`                   | News and announcements archive.                                           | [News and tourism](site-hierarchy/news-tourism.md) |
| `/news/:slug`             | News detail.                                                              | [News and tourism](site-hierarchy/news-tourism.md) |
| `/tourism`                | Visitor information and local stories.                                    | [News and tourism](site-hierarchy/news-tourism.md) |
| `/tourism/:slug`          | Tourism story detail.                                                     | [News and tourism](site-hierarchy/news-tourism.md) |

## Transparency and public records

`/transparency` is the overview. Category pages share an archive component and the transparency layout.

| Route                                   | Records                                                         |
| --------------------------------------- | --------------------------------------------------------------- |
| `/transparency`                         | Overview and category navigation.                               |
| `/transparency/ordinances`              | Ordinances.                                                     |
| `/transparency/resolutions`             | Resolutions.                                                    |
| `/transparency/executive-orders`        | Executive orders.                                               |
| `/transparency/memorandums`             | Memoranda.                                                      |
| `/transparency/full-disclosure`         | Financial and operational disclosures.                          |
| `/transparency/bids-awards`             | Procurement notices and awards.                                 |
| `/transparency/forms`                   | Downloadable forms.                                             |
| `/transparency/document/:slug?kind=...` | Shared public-record detail; `kind` selects its return archive. |

See [Transparency](site-hierarchy/transparency.md) for archive behavior and the CMS connection.

## Staff workspace

| Route                | Purpose                                            |
| -------------------- | -------------------------------------------------- |
| `/login`             | Staff sign-in; success routes to `/admin/content`. |
| `/admin`             | Authenticated editorial workspace shell.           |
| `/admin/content`     | Create, edit, and publish public content.          |
| `/admin/`            | Redirects to `/admin/content`.                     |
| `/admin/permissions` | Redirects to `/admin/content`.                     |
| `/admin/roles`       | Redirects to `/admin/content`.                     |

See [Staff and CMS](site-hierarchy/staff-cms.md) for the protected route and content flow.

## Navigation nodes

- [Header and navigation](site-hierarchy/header-navigation.md) — global navigation destinations and footer links.
- [Business logic](business-logic/public-content.md) — content kinds and current public/CMS data boundary.
