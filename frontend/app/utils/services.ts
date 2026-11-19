export interface PublicServiceLink {
  label: string
  description: string
  to: string
  icon: string
}

export const publicServiceLinks: PublicServiceLink[] = [
  {
    label: 'Forms and Applications',
    description: 'Browse downloadable municipal forms.',
    to: '/transparency/forms',
    icon: 'i-lucide-file-down'
  },
  {
    label: 'Government Updates',
    description: 'Read current public notices and actions.',
    to: '/about/actions',
    icon: 'i-lucide-megaphone'
  },
  {
    label: 'Ordinances',
    description: 'Find local laws and ordinances.',
    to: '/transparency/ordinances',
    icon: 'i-lucide-scroll-text'
  },
  {
    label: 'Resolutions',
    description: 'Browse resolutions of the municipality.',
    to: '/transparency/resolutions',
    icon: 'i-lucide-file-check-2'
  },
  {
    label: 'Bids and Awards',
    description: 'Review procurement notices and awards.',
    to: '/transparency/bids-awards',
    icon: 'i-lucide-briefcase-business'
  },
  {
    label: 'Full Disclosure',
    description: 'Access municipal disclosure documents.',
    to: '/transparency/full-disclosure',
    icon: 'i-lucide-landmark'
  },
  {
    label: 'News and Announcements',
    description: 'See recent municipal news and events.',
    to: '/news',
    icon: 'i-lucide-newspaper'
  },
  {
    label: 'Tourism Information',
    description: 'Explore visitor information and local stories.',
    to: '/tourism',
    icon: 'i-lucide-map'
  }
]
