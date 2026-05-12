# LGU Consolacion Website

A modern municipal website for the **Municipality of Consolacion** built with **Nuxt 4 + Nuxt UI** (frontend), featuring responsive design and comprehensive civic services information.

## Features

- **Modern Design** — Clean, responsive interface built with Nuxt 4 and Nuxt UI components.
- **Custom Theme** — Branded color scheme (#F57056 primary coral, #F6B82B secondary golden).
- **Typography** — Domine font for hero sections with professional municipal appearance.
- **Responsive Layout** — Mobile-first design that works seamlessly across all devices.
- **Component Architecture** — Modular Vue components for services, contact, news, and hero sections.
- **Performance Optimized** — Fast loading with proper font optimization and asset management.
- **Accessibility** — Semantic HTML5 structure with proper ARIA labels and keyboard navigation.

## Prerequisites

| Dependency | Version | Notes               |
| ---------- | ------- | ------------------- |
| Node.js    | ≥ 20    | via nvm recommended |
| pnpm       | ≥ 10    | `npm i -g pnpm`     |

## Quick Start

### 1. Clone and install dependencies

```bash
git clone git@github.com:jimmyyyricks/lgu-consolacion.git
cd lgu-consolacion
cd frontend
pnpm install
```

### 2. Start the development server

```bash
cd frontend
pnpm dev
```

The browser will open to `http://localhost:3000` displaying the LGU Consolacion website.

### 3. Build for production

```bash
cd frontend
pnpm build
# Start the production server
node .output/server/index.mjs
```

## Project Structure

```
lgu-consolacion/
├── frontend/
│   ├── app/
│   │   ├── components/
│   │   │   ├── lgu/           # LGU-specific components
│   │   │   │   ├── LguHero.vue
│   │   │   │   ├── LguServices.vue
│   │   │   │   ├── LguContact.vue
│   │   │   │   └── LguNews.vue
│   │   │   └── ...
│   │   ├── layouts/
│   │   │   └── default.vue    # Main layout with header/footer
│   │   ├── pages/
│   │   │   └── index.vue      # Home page
│   │   └── assets/
│   │       ├── css/
│   │       └── images/
│   ├── public/
│   │   ├── fonts/             # Custom fonts (Domine)
│   │   └── images/
│   ├── nuxt.config.ts
│   ├── app.config.ts
│   └── package.json
├── .gitignore
├── install.sh
├── run.sh
└── README.md
```

## Components

### LguHero

- Main hero section with municipality branding
- Custom Domine font typography
- Responsive design with image carousel
- Call-to-action buttons for services and contact

### LguServices

- Comprehensive municipal services display
- Grid layout with service cards
- Icons and descriptions for each service

### LguContact

- Contact information and office details
- Individual cards for each contact method
- Phone numbers and address information

### LguNews

- Latest news and announcements
- Blog post layout with horizontal orientation
- "View All News" navigation

## Customization

### Colors

The website uses a custom color theme defined in `app.config.ts`:

- **Primary**: `#F57056` (coral red)
- **Secondary**: `#F6B82B` (golden yellow)
- **Neutral**: `slate`

### Typography

- **Domine**: Custom serif font for hero titles
- **Inter**: System sans-serif for body text

### Images

- **Hero Images**: Place in `frontend/public/images/`
- **Logo**: Update favicon and branding assets

## Tech Stack

**Frontend:** Nuxt 4, Vue 3, Nuxt UI 4, Pinia, Tailwind CSS 4, VueUse, Nuxt Fonts

**Development:** pnpm, TypeScript, ESLint, Playwright (E2E Testing)
