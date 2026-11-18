# About Consolacion

The About area uses a shared tab layout for municipal background and leadership pages.

| Tab                      | Route                     | Contents                                                                                                            |
| ------------------------ | ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Citizen's Charter        | `/about`                  | Mandate, vision, mission, objectives, programs, service pledge, feedback process, and other-office service summary. |
| Office of the Mayor      | `/about/mayor`            | Mayor's Office contact and five service summaries from the 2026 Charter.                                            |
| Office of the Vice Mayor | `/about/vice-mayor`       | Vice Mayor's message, office contact, and Sangguniang Bayan service summaries.                                      |
| Municipal Officials      | `/about/officials`        | Elected Sangguniang Bayan roster.                                                                                   |
| Office Directory         | `/about/office-directory` | Legacy hotlines and office numbers, with a link to the official 2026 Charter directory.                             |
| Government Actions       | `/about/actions`          | Notices and action archive; details use `/about/actions/:slug`.                                                     |

The Citizen's Charter tab uses `LguAbout`, `LguCityPrograms`, and `LguCharterDetails`. Mandate, vision, mission, and objectives appear once. The Mayor and Vice Mayor tabs summarize their Charter services and link to the full 2026 edition for requirements, fees, and processing steps. The Office Directory is a separate page.

Office contacts come from `municipal-information.ts`.

See [Header and navigation](header-navigation.md) for the global About link and [Site routes](../site-routes.md) for the full route map.
