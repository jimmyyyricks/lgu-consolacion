export const siteRoutes = {
  home: '/',
  about: '/about',
  actions: '/about/actions',
  officials: '/about/officials',
  officeDirectory: '/about/office-directory',
  news: '/news',
  transparency: '/transparency',
  ordinances: '/transparency/ordinances',
  resolutions: '/transparency/resolutions',
  executiveOrders: '/transparency/executive-orders',
  memorandums: '/transparency/memorandums',
  fullDisclosure: '/transparency/full-disclosure',
  bidsAwards: '/transparency/bids-awards',
  forms: '/transparency/forms',
  tourism: '/tourism',
  login: '/login'
}

export const headerNavigation = [
  {
    label: 'Home',
    to: siteRoutes.home
  },
  {
    label: 'About',
    to: siteRoutes.about
  },
  {
    label: 'News',
    to: siteRoutes.news
  },
  {
    label: 'Transparency',
    to: siteRoutes.transparency,
    children: [
      {
        label: 'Ordinances',
        icon: 'i-lucide-scale',
        description: 'Local laws enacted by the Sangguniang Bayan.',
        to: siteRoutes.ordinances
      },
      {
        label: 'Resolutions',
        icon: 'i-lucide-file-check-2',
        description: 'Official resolutions and legislative actions.',
        to: siteRoutes.resolutions
      },
      {
        label: 'Executive Orders',
        icon: 'i-lucide-file-pen-line',
        description: 'Published executive issuances.',
        to: siteRoutes.executiveOrders
      },
      {
        label: 'Memoranda',
        icon: 'i-lucide-files',
        description: 'Published municipal memoranda.',
        to: siteRoutes.memorandums
      },
      {
        label: 'Full Disclosure',
        icon: 'i-lucide-chart-no-axes-combined',
        description: 'Publicly released financial and operational records.',
        to: siteRoutes.fullDisclosure
      },
      {
        label: 'Bids and Awards',
        icon: 'i-lucide-gavel',
        description: 'Procurement notices and award information.',
        to: siteRoutes.bidsAwards
      },
      {
        label: 'Downloadable Forms',
        icon: 'i-lucide-file-down',
        description: 'Forms made available by municipal offices.',
        to: siteRoutes.forms
      }
    ]
  },
  { label: 'Tourism', to: siteRoutes.tourism }
]

export const footerColumns = [
  {
    label: 'Services and information',
    children: [
      { label: 'All Services and Links', to: `${siteRoutes.home}#services` },
      { label: 'Forms and Applications', to: siteRoutes.forms },
      { label: 'Government Updates', to: siteRoutes.actions }
    ]
  },
  {
    label: 'About',
    children: [
      { label: 'About Consolacion', to: siteRoutes.about },
      { label: "Citizen's Charter", to: `${siteRoutes.about}#citizens-charter` },
      { label: 'Sangguniang Bayan', to: siteRoutes.officials },
      { label: 'Office Directory', to: siteRoutes.officeDirectory },
      { label: 'News and Announcements', to: siteRoutes.news },
      { label: 'Tourism', to: siteRoutes.tourism }
    ]
  },
  {
    label: 'Public records',
    children: [
      { label: 'Transparency Portal', to: siteRoutes.transparency },
      { label: 'Ordinances and Resolutions', to: siteRoutes.ordinances },
      { label: 'Bids and Awards', to: siteRoutes.bidsAwards }
    ]
  }
]
