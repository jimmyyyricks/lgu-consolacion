import type { PublicContentItem, PublicContentKind } from '~/composables/usePublicContent'

type StaticContentEntry = Pick<
  PublicContentItem,
  'slug' | 'kind' | 'title' | 'summary' | 'body'
> & Partial<Pick<
  PublicContentItem,
  'document_number' | 'category' | 'image_url' | 'featured' | 'record_date' | 'published_at'
>>

const migratedContent: StaticContentEntry[] = [
  {
    slug: 'committee-meeting-land-use-jan-16-2026',
    kind: 'news',
    title: 'Committee meeting on land use (Jan. 16, 2026) 1:30 PM',
    summary: 'Sangguniang Bayan committee meeting notice for the Committee on Land Use.',
    body: 'The legacy site listed this committee meeting for January 16, 2026 at 1:30 p.m. at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2026-01-16',
    published_at: '2026-01-16T00:00:00',
    featured: true
  },
  {
    slug: 'committee-meeting-environment-jan-15-2026',
    kind: 'news',
    title: 'Committee meeting on environment (Jan. 15, 2026) 1:00 PM',
    summary: 'Sangguniang Bayan committee meeting notice for the Committee on Environment.',
    body: 'The legacy site listed this committee meeting for January 15, 2026 at 1:00 p.m. at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2026-01-15',
    published_at: '2026-01-16T00:00:00',
    featured: true
  },
  {
    slug: 'committee-meeting-land-use-jan-9-2026',
    kind: 'news',
    title: 'Committee meeting on land use (Jan. 9, 2026) 3:30 PM',
    summary: 'Sangguniang Bayan committee meeting notice for the Committee on Land Use.',
    body: 'The legacy site listed this committee meeting for January 9, 2026 at 3:30 p.m. at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2026-01-09',
    published_at: '2026-01-09T00:00:00',
    featured: true
  },
  {
    slug: 'committee-meeting-finance-jan-9-2026',
    kind: 'news',
    title: 'Committee meeting on finance (Jan. 9, 2026) 1:00 PM',
    summary: 'Sangguniang Bayan committee meeting notice for the Committee on Finance.',
    body: 'The legacy site listed this committee meeting for January 9, 2026 at 1:00 p.m. at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2026-01-09',
    published_at: '2026-01-09T00:00:00',
    featured: true
  },
  {
    slug: 'committee-meeting-tourism-jan-8-2026',
    kind: 'news',
    title: 'Committee meeting on tourism (Jan. 8, 2026) 1:00 PM',
    summary: 'Sangguniang Bayan committee meeting notice for the Committee on Tourism.',
    body: 'The legacy site listed this committee meeting for January 8, 2026 at 1:00 p.m. at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2026-01-08',
    published_at: '2026-01-09T00:00:00',
    featured: true
  },
  {
    slug: 'committee-meeting-environment-oct-22-2025',
    kind: 'news',
    title: 'Committee meeting on environment (Oct. 22, 2025) 1:00 PM',
    summary: 'Sangguniang Bayan committee meeting notice for the Committee on Environment.',
    body: 'The legacy site listed this committee meeting for October 22, 2025 at 1:00 p.m. at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2025-10-22',
    published_at: '2025-10-22T00:00:00'
  },
  {
    slug: 'committee-meeting-traffic-peace-order-oct-15-2025',
    kind: 'news',
    title: 'Committee meeting on traffic management / peace and order (Oct. 15, 2025)',
    summary: 'Sangguniang Bayan committee meeting notice for traffic management and peace and order.',
    body: 'The legacy site listed this committee meeting for October 15, 2025 at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2025-10-15',
    published_at: '2025-10-15T00:00:00'
  },
  {
    slug: 'committee-meeting-land-use-oct-2-2025',
    kind: 'news',
    title: 'Committee meeting on land use (Oct. 2, 2025) 1:00 PM',
    summary: 'Sangguniang Bayan committee meeting notice for the Committee on Land Use.',
    body: 'The legacy site listed this committee meeting for October 2, 2025 at 1:00 p.m. at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2025-10-02',
    published_at: '2025-10-02T00:00:00'
  },
  {
    slug: 'committee-meeting-peace-order-sep-12-2025',
    kind: 'news',
    title: 'Committee meeting on peace and order (Sept. 12, 2025)',
    summary: 'Sangguniang Bayan committee meeting notice for the Committee on Peace and Order.',
    body: 'The legacy site listed this committee meeting for September 12, 2025 at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2025-09-12',
    published_at: '2025-09-12T00:00:00'
  },
  {
    slug: 'committee-meeting-accreditation-finance-land-use-sep-11-2025',
    kind: 'news',
    title: 'Committee meeting on accreditation / finance / land use (Sept. 11, 2025)',
    summary: 'Sangguniang Bayan committee meeting notice covering accreditation, finance, and land use.',
    body: 'The legacy site listed this committee meeting at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2025-09-11',
    published_at: '2025-09-12T00:00:00'
  },
  {
    slug: 'committee-meeting-tourism-laws-sep-10-2025',
    kind: 'news',
    title: 'Committee meeting on tourism and laws (Sept. 10, 2025) 1:00 PM, 2:00 PM',
    summary: 'Sangguniang Bayan committee meeting notice for Tourism and Laws.',
    body: 'The legacy site listed this committee meeting for September 10, 2025 at 1:00 p.m. and 2:00 p.m. at the 3rd Floor, SB Cubicle.',
    category: 'Activities',
    record_date: '2025-09-10',
    published_at: '2025-09-11T00:00:00'
  },
  {
    slug: 'civil-society-organization-accreditation-notice-2025',
    kind: 'news',
    title: 'Notice to the public – Accreditation of Civil Society Organization (Aug. 27, 2025) 1:00 PM',
    summary: 'Public notice concerning Civil Society Organization accreditation.',
    body: 'The legacy site listed this public notice for August 27, 2025 at 1:00 p.m. at the 3rd Floor.',
    category: 'Notice',
    record_date: '2025-08-27',
    published_at: '2025-08-20T00:00:00'
  },
  {
    slug: 'citizens-charter-2024-announcement',
    kind: 'news',
    title: 'LGU-Consolacion, Cebu – Citizen\'s Charter 2024',
    summary: 'The Municipality of Consolacion published the second edition of its 2024 Citizen\'s Charter.',
    body: 'The legacy site listed the LGU-Consolacion Citizen\'s Charter 2024 on May 29, 2025. The charter includes the municipal mandate, vision, mission, service pledge, and office service procedures.',
    category: 'News',
    record_date: '2025-05-29',
    published_at: '2025-05-29T00:00:00'
  },
  {
    slug: 'public-hearing-proposed-zoning-ordinance-2025',
    kind: 'news',
    title: 'Public hearing on the proposed zoning ordinance (May 27, 2025)',
    summary: 'The legacy site announced a public hearing on the proposed zoning ordinance.',
    body: 'The Sangguniang Bayan news archive listed a public hearing on the proposed zoning ordinance for May 27, 2025.',
    category: 'Public hearing',
    record_date: '2025-05-27',
    published_at: '2025-05-28T00:00:00'
  },
  {
    slug: 'last-day-ojt-privilege-speech-2025',
    kind: 'news',
    title: 'Last day of OJT – Privilege Speech (May 8, 2025)',
    summary: 'A Sangguniang Bayan news item about the last day of the on-the-job training program.',
    body: 'The legacy site listed this news item on May 9, 2025 with the title “Last Day of OJT – Privilege Speech (May 8, 2025)”.',
    category: 'News',
    record_date: '2025-05-08',
    published_at: '2025-05-09T00:00:00'
  },
  {
    slug: 'notice-of-award-mixed-use-office-building-2025',
    kind: 'news',
    title: 'Notice of Award – Mixed-Use Office Building',
    summary: 'The legacy site published a notice of award for the Mixed-Use Office Building.',
    body: 'The Sangguniang Bayan news archive listed this notice on February 17, 2025. No award document is attached in this static migration.',
    category: 'Notice of award',
    record_date: '2025-02-17',
    published_at: '2025-02-17T00:00:00'
  },
  {
    slug: 'bidding-documents-mixed-use-office-building-2024',
    kind: 'news',
    title: 'Bidding Documents and Draft Joint Venture Agreement for the Invitation to Submit Comparative Proposals of 9-Storey Mixed-Use Office Building',
    summary: 'An announcement listing bidding documents and a draft joint venture agreement for the proposed office building.',
    body: 'The legacy site listed this announcement on November 25, 2024. No bidding files are attached in this static migration.',
    category: 'Announcement',
    record_date: '2024-11-25',
    published_at: '2024-11-25T00:00:00'
  },
  {
    slug: 'mixed-use-office-building-notice-of-award-2025',
    kind: 'bid',
    title: 'NOTICE OF AWARD MIXED-USE OFFICE BUILDING',
    summary: 'Notice title transcribed from the legacy Sangguniang Bayan news archive.',
    body: 'The legacy site listed this notice on February 17, 2025. No award document is attached in this static migration.',
    category: 'Notice of award',
    record_date: '2025-02-17',
    published_at: '2025-02-17T00:00:00'
  },
  {
    slug: 'mixed-use-office-building-bidding-documents-2024',
    kind: 'bid',
    title: 'Bidding Documents and Draft Joint Venture Agreement for the Invitation to Submit Comparative Proposals of 9-Storey Mixed-Use Office Building',
    summary: 'Procurement title transcribed from the legacy Sangguniang Bayan announcements archive.',
    body: 'The legacy site listed this announcement on November 25, 2024. No bidding documents are attached in this static migration.',
    category: 'Procurement announcement',
    record_date: '2024-11-25',
    published_at: '2024-11-25T00:00:00'
  },
  {
    slug: 'clup-2024-2033-adoption',
    kind: 'government_action',
    title: 'Adoption, the CLUP 2024–2033 and Enactment Corresponding Zoning Ordinance',
    summary: 'The Sangguniang Bayan published the Comprehensive Land Use Plan 2024–2033 adoption and zoning ordinance item.',
    body: 'The legacy site listed this item as municipal news on May 16, 2025. The page linked to the Comprehensive Land Use Plan 2024–2033 document.',
    category: 'Municipal planning',
    record_date: '2025-05-16',
    published_at: '2025-05-16T00:00:00'
  },
  {
    slug: 'sarok-festival',
    kind: 'tourism',
    title: 'Sarok Festival',
    summary: 'Consolacion\'s festival celebrates the sarok, a traditional woven hat associated with local craft and community identity.',
    body: 'The Sarok Festival is a cultural celebration of Consolacion. The Cebu Provincial Government describes the sarok as a woven hat made from bamboo strips and dried banana leaves.',
    category: 'Culture and heritage'
  },
  {
    slug: 'consolacion-heritage-sites',
    kind: 'tourism',
    title: 'Heritage places in Consolacion',
    summary: 'The municipality\'s land-use plan identifies San Narciso Church, the Old Municipal Town Hall, and Gabaldon school buildings as built heritage.',
    body: 'These heritage places are identified in the Consolacion Comprehensive Land Use Plan 2024–2033. Confirm access and visiting arrangements with the relevant site before traveling.',
    category: 'Local heritage'
  },
  {
    slug: 'villarocca-lake',
    kind: 'tourism',
    title: 'Villarocca Lake',
    summary: 'A wetland and natural heritage feature noted in the municipality\'s Comprehensive Land Use Plan.',
    body: 'Villarocca Lake is identified in the Consolacion Comprehensive Land Use Plan 2024–2033 as a wetland with aquatic resources. Confirm access and conditions locally before visiting.',
    category: 'Nature'
  },
  ...([
    ['ordinance-35-2024', 'PROVIDING A COMPREHENSIVE YOUTH WELFARE & DEV\'T. CODE OF MUN. GOV\'T.', '35, S.2024'],
    ['ordinance-34-2024', 'CREATING POSITION OF ADMINISTRATIVE AIDE VI (LABOR FOREMAN) UNDER MPDO', '34, S.2024'],
    ['ordinance-33-2024', 'CREATING POSITION OF LOCAL TREASURY OPERATIONS OFFICER I UNDER MUN. TREASURER\'S OFFICE.', '33, S.2024'],
    ['ordinance-32-2024', 'ABOLISHING THE OFFICE & ALL CREATED POSITIONS UNDER CONSOLACION COMMUNITY COLLEGE (CCC).', '32, S.2024'],
    ['ordinance-26-2024', 'AMENDATORY ORDINANCE OF MARKET STALL TRANSFER OF PRIVILEGE-AWARD.', '26, S.2024'],
    ['ordinance-25-2024', 'HONORING & GRANTING CASH INCENTIVES TO OCTOGENARIANS, NONAGENARIANS,& CENTENARIANS TO QUALIFIED SENIOR CITIZENS.', '25, S.2024'],
    ['ordinance-09-2006', 'FIXING PASSENGERS\' FARE FOR PUBLIC UTILITY VEHICLES OR TRICYCLES FOR HIRE PLYING TAYUD-CONSOLACION ROUTE.', '09, S.2006'],
    ['ordinance-01-2006', 'DESIGNATING CERTAIN AREAS IN NAT\'L. H-WAY & MUN. ROAD AS PEDESTRIAN LANES & PROHIBITING ALL PERSONS TO CROSS THE STREET (ANTI-JAYWALKING ORD.)', '01, S.2006'],
    ['ordinance-06-2002', 'RE-ALIGNED (P 71,972.60) & (85K) FOR OFFICE OF THE ACCOUNTANT\'S CAPITAL OUTLAY APP. FOR PURCHASE OF PRINTER & COMPUTER', '06, S.2002'],
    ['ordinance-04-2003', 'FIXING FEES & CHARGES ON APPLICATION FOR REGISTRATION OF BRGY. MICRO BUSINESS ENTERPRISES (BMBE\'S) ACT OF 2002', '04, S.2003'],
    ['ordinance-01-a-2000', 'APPROVING SUPPLEMENTAL BUDGET NO. 01-A OF THE MOC CY 2000', '01-A-2000, S.2000'],
    ['ordinance-02-2000', 'AMENDING ORD. NO. 02, S. 1999 ON IMPOSITION OF REGULATORY FEES ON THE TRANSFER OF MARKET STALLS & TARIMA', '02, S.2000'],
    ['ordinance-05-2000', 'CREATING THE BRGY. PREQUALIFICATION, BIDDING & AWARDS COMMITTEE (PBAC) FOR 21 BRGYS.', '05, S.2000'],
    ['ordinance-01-2000', 'ADOPTING & ESTABLISHING CERTAIN PROCEDURES IN PROCESSING & APPROVAL OF APPLICATIONS FOR SUBDIVISIONS, KNOWN AS LOCAL GOV\'T. CODE', '01, S.2000'],
    ['ordinance-03-1992', 'ENACTING LOCAL TAX ORD. LEVYING A COMMUNITY TAX SEC. 156 RA 7160 (LOCAL GOV\'T. CODE)', '03, S.1992'],
    ['ordinance-07-1992', 'ENACTING AN ORD. FORMALLY CREATING PEOPLE\'S LAW ENFORCEMENT BOARD OF MOC (PLEB ORD.)', '07, S.1992'],
    ['ordinance-04-1992', 'APPROVING ANNUAL BUDGET OF CASILI.', '04-1992, S.1992']
  ] as const).map(([slug, title, number]) => ({
    slug,
    kind: 'ordinance' as const,
    title,
    document_number: `Ordinance No. ${number}`,
    summary: 'Title transcribed from the legacy Sangguniang Bayan ordinance index. No ordinance file is included in this static listing.',
    body: `This static entry preserves the title shown in the legacy ordinance index. It contains no ordinance file and is not a substitute for the enacted text or a certified copy.`,
    category: 'Ordinance'
  })),
  ...([
    ['resolution-99-2024', '1ST READING ENACTING ORD. CREATING 2 POSITIONS OF TRAFFIC AIDE I UNDER MUN. ADMINISTRATOR\'S OFFICE', '99, S.2024'],
    ['resolution-98-2024', '1ST READING ENACTING ORD. CREATING POSITION OF FOREST RANGER UNDER MENRO', '98, S.2024'],
    ['resolution-97-2024', '1ST READING ENACTING AN ORD. CREATING 2 POSITIONS OF FARM WORKER II UNDER MUN. AGRICULTURAL OFFICE', '97, S.2024'],
    ['resolution-96-2024', '1ST READING ENACTING ORD. CREATING POSITION ADMINISTRATIVE OFFICER IV (BUDGET OFFICER II) UNDER MBO', '96, S.2024'],
    ['resolution-95-2024', '1ST READING ENACTING APP ORD. SUPPLEMENTAL BUDGET NO. 01, FISCAL YEAR 2024 (Php 199,858,931.16)', '95, S.2024'],
    ['resolution-94-2024', 'RESETTING SCHEDULED DATE OF REG. SESSION EARLIER FROM MARCH 28 TO MARCH 27, 2024 @ 10AM', '94, S.2024'],
    ['resolution-93-2024', 'REQUESTING V-MAYOR TO CONVENE LEGISLATIVE EDUC. & ADVOCACY PLANNING COMMITTEE (LEAP) IN LEGISLATIVE AWARENESS WEEK', '93, S.2024'],
    ['resolution-92-2024', 'APPROVING ANNUAL BUDGET CY 2024 OF SK DANGLAG (P 1,325,137.67)', '92, S.2024'],
    ['resolution-91-2024', 'APPROVING ANNUAL BUDGET CY 2024 OF SK CABANGAHAN (P 805,768.86)', '91, S.2024'],
    ['resolution-90-2024', 'APPROVING ANNUAL BUDGET CY 2024 OF SACSAC (P 4,792,664.21)', '90, S.2024'],
    ['resolution-385-2024', 'APPROVING JOINT VENTURE AGREEMENT (JVA) PROPOSED PPP-PROJECT, PUBLIC-PRIVATE PARTNERSHIP (PPPs)', '385, S.2024'],
    ['resolution-384-2024', 'DECLARING NO SESSION ON OCT. 31, 2024 IN PREPARATION FOR THE ALL SOUL\'S & ALL SAINT\'S DAY', '384, S.2024'],
    ['resolution-383-2024', 'APPROVING RE-ALIGNMENT FROM BALANCES CY 2024 APPROPRIATION UNDER OFFICE OF SANGGUNIANG BAYAN', '383, S.2024'],
    ['resolution-382-2024', 'APPROVING SUPPLEMENTAL LDRRM PLAN CY 2024 (P 3,215,761.87).', '382, S.2024'],
    ['resolution-381-2024', 'AUTHORIZING MAYOR & TREASURER TO OPEN DEPOSIT ACCOUNT WITH LAND BANK (LBP) & DESIGNATE AS OFFICIAL SIGNATORIES', '381, S.2024'],
    ['resolution-375-2024', 'CONGRATULATING HENRICK BALTAZAR TAUTOAN, 1ST PLACE (BEST DECORATED FLOAT) DURING PASIGARBO SA SUGBO 2024', '375, S.2024'],
    ['resolution-13-2024', 'MOA FOR WORK IMMERSION PARTNERSHIP WITH SOTERO B. CABAHUG FORUM FOR LITERACY', '13, S.2024']
  ] as const).map(([slug, title, number]) => ({
    slug,
    kind: 'resolution' as const,
    title,
    document_number: `Resolution No. ${number}`,
    summary: 'Title transcribed from the legacy Sangguniang Bayan resolution index. No resolution file is included in this static listing.',
    body: 'This static entry preserves the title shown in the legacy resolution index. It contains no resolution file and is not a substitute for the approved resolution or a certified copy.',
    category: 'Resolution'
  })),
  ...[
    'Application for Development and/or Building Permit of Project Under B.P. 220',
    'Application for Preliminary Approval and Locational Clearance of Project Under B.P. 220',
    'Application for Approval of Simple Subdivision',
    'Accreditation Form',
    'Application for Alteration of Plan',
    'Application for Development Permits Project Under P.D. 957',
    'Application for Preliminary Approval and Location Clearance of Project Under P.D. 957'
  ].map((title, index) => ({
    slug: `legacy-form-${index + 1}`,
    kind: 'form' as const,
    title,
    summary: 'Form title migrated from the legacy downloadable-files list. The original file is not included in this static listing.',
    body: 'This entry preserves the form title only. Contact the relevant municipal office for a current copy and requirements.',
    category: 'Application form',
    record_date: '2024-03-17',
    published_at: '2024-03-17T00:00:00'
  }))
]

const staticPublicContent: PublicContentItem[] = migratedContent.map((item) => {
  const timestamp = item.published_at || '2025-05-16T00:00:00'
  return {
    id: item.slug,
    slug: item.slug,
    kind: item.kind,
    title: item.title,
    document_number: item.document_number || null,
    summary: item.summary,
    body: item.body,
    category: item.category || null,
    image_url: item.image_url || null,
    featured: item.featured || false,
    record_date: item.record_date || null,
    status: 'published',
    drive_file_id: null,
    created_at: timestamp,
    updated_at: timestamp,
    published_at: item.published_at || null
  }
})

export const getStaticPublicContent = (kind?: PublicContentKind) =>
  kind ? staticPublicContent.filter(item => item.kind === kind) : staticPublicContent

export const getStaticPublicContentBySlug = (slug: string) =>
  staticPublicContent.find(item => item.slug === slug)
