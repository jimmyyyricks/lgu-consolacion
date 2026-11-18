# Transparency and Public Records

`/transparency` is the records landing page. Its sticky category navigation and overview cards lead to the archives below.

| Route | Content kind | Purpose |
| --- | --- | --- |
| `/transparency/ordinances` | `ordinance` | Local laws enacted by the Sangguniang Bayan. |
| `/transparency/resolutions` | `resolution` | Municipal resolutions and legislative actions. |
| `/transparency/executive-orders` | `executive_order` | Executive orders. |
| `/transparency/memorandums` | `memorandum` | Municipal memoranda. |
| `/transparency/full-disclosure` | `disclosure` | Financial and operational disclosures. |
| `/transparency/bids-awards` | `bid` | Procurement notices and award records. |
| `/transparency/forms` | `form` | Downloadable municipal forms. |

Archives use the shared `PublicContentArchive` component. Visitors can search, filter by year, paginate, and open a record preview. The current archive identifies document entries as a static title index; original copies may need to be requested from the relevant office.

## Record detail

`/transparency/document/:slug?kind=...` displays a public-record detail. The `kind` query selects the return archive. A Google Drive preview is shown when the record has a Drive file ID.

The [services directory](services.md), homepage, header, and footer link into this section. Content kinds and the current data boundary are in [Business logic](../business-logic/public-content.md); the staff publishing path is in [Staff and CMS](staff-cms.md).
