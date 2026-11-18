import { expect, test } from '@playwright/test'

test('home page presents news, services, updates, tourism and public records', async ({ page }) => {
  const response = await page.goto('/')
  expect(response?.ok()).toBeTruthy()
  expect(await page.content()).toContain('Municipality of Consolacion')
  const carouselSection = page.locator('section[aria-labelledby="news-carousel-heading"]')
  const carousel = carouselSection.getByRole('region', { name: 'Sangguniang Bayan activity notices' })
  await expect(carousel).toBeVisible()
  const slideCount = await carousel.locator('[data-slot="item"]').count()
  await expect(carousel.getByText(/Committee meeting on/).first()).toBeVisible()
  await expect(carouselSection.getByText(`1 of ${slideCount}`, { exact: true })).toBeVisible()
  if (slideCount > 1) {
    await carousel.locator('[data-slot="next"]').click()
    await expect(carouselSection.getByText(`2 of ${slideCount}`, { exact: true })).toBeVisible()
  }
  await expect(page.getByRole('heading', { name: 'Services and useful links' })).toBeVisible()
  await expect(page.getByRole('textbox', { name: 'Search services and links' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Weather and reminders' })).toBeVisible()
  await expect(page.getByText('Live weather updates are not available on this site yet.')).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Tourism in Consolacion' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Government and planning updates' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Public records' }).first()).toBeVisible()

  await page.goto('/transparency/ordinances')
  await expect(page.getByRole('heading', { name: 'Municipal Ordinances' })).toBeVisible()
  await expect(page.getByRole('textbox', { name: 'Search public records' })).toBeVisible()
  await expect(page.getByText('Static title index')).toBeVisible()
  await page.getByRole('link', { name: /ORDINANCE NO\. 35/ }).click()
  const preview = page.getByRole('dialog')
  await expect(preview).toContainText('ORDINANCE NO. 35')
  await expect(preview).toContainText('PDF preview unavailable')
  await preview.getByRole('button', { name: 'Close' }).click()
  await page.getByRole('textbox', { name: 'Search public records' }).fill('youth welfare')
  await expect(page.getByRole('link', { name: /ORDINANCE NO\. 35/ })).toBeVisible()
  await page.getByRole('button', { name: 'Filter by publication year' }).click()
  await page.getByRole('option', { name: '2024' }).click()
  await expect(page.getByRole('link', { name: /ORDINANCE NO\. 35/ })).toBeVisible()
  await page.goto('/transparency/resolutions')
  await expect(page.getByRole('heading', { name: 'Municipal Resolutions' })).toBeVisible()
  await expect(page.getByRole('link', { name: /TRAFFIC AIDE I/ })).toBeVisible()
  await page.getByRole('link', { name: 'Forms', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Downloadable forms' })).toBeVisible()

  await page.goto('/tourism')
  await expect(page.getByRole('heading', { name: 'Tourism in Consolacion' })).toBeVisible()
  await expect(page.getByRole('textbox', { name: 'Search tourism stories' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Local guides and community stories' })).toBeVisible()
})

test('homepage presents quick links and community actions separately from About content', async ({ page }) => {
  await page.goto('/')

  const quickLinks = page.getByRole('region', { name: 'Quick links' })
  await expect(quickLinks.getByRole('link', { name: 'Find a municipal service' })).toHaveAttribute('href', '/#services')
  await expect(quickLinks.getByRole('link', { name: 'Get a municipal form' })).toHaveAttribute('href', '/transparency/forms')
  await expect(quickLinks.getByRole('link', { name: 'Read a public notice' })).toHaveAttribute('href', '/about/actions')
  await expect(quickLinks.getByRole('link', { name: 'Access public records' })).toHaveAttribute('href', '/transparency')
  await expect(page.getByRole('heading', { name: 'Resident guides' })).toHaveCount(0)
  const hero = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Welcome to Consolacion' }) })
  expect(await hero.evaluate((element) => {
    const description = element.querySelector('[data-slot="description"]')!
    const cards = element.querySelector('[role="region"][aria-label="Quick links"]')!
    const actions = element.querySelector('[data-slot="links"]')!
    return Boolean(
      (description.compareDocumentPosition(cards) & Node.DOCUMENT_POSITION_FOLLOWING)
      && (cards.compareDocumentPosition(actions) & Node.DOCUMENT_POSITION_FOLLOWING)
    )
  })).toBeTruthy()
  await expect(page.getByRole('heading', { name: 'Municipal programs' })).toHaveCount(0)
  await expect(page.getByRole('heading', { name: 'A Message from the Vice Mayor' })).toHaveCount(0)
  await expect(page.getByRole('heading', { name: 'Sangguniang Bayan Members' })).toHaveCount(0)
  await expect(page.getByRole('heading', { name: 'Objectives' })).toHaveCount(0)
  await expect(page.getByRole('heading', { name: 'People\'s Corner' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Email the municipal government' })).toHaveAttribute(
    'href',
    'mailto:info@consolacion.gov.ph'
  )
})

test('homepage fills the first screen and offers a scroll-to-top button', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })

  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 900 })
    await page.goto('/')
    await page.waitForFunction(() => Boolean(
      (document.querySelector('h1') as
        | (HTMLElement & { __vueParentComponent?: unknown })
        | null)?.__vueParentComponent
    ))

    const hero = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Welcome to Consolacion' }) })
    const bottom = await hero.evaluate(element => element.getBoundingClientRect().bottom)
    expect(bottom).toBeGreaterThanOrEqual(899)

    const backToTop = page.getByRole('button', { name: 'Scroll to top' })
    await expect(backToTop).toHaveCount(0)
    await page.evaluate(() => window.scrollTo(0, 800))
    await expect(backToTop).toBeVisible()
    await backToTop.focus()
    await page.keyboard.press('Enter')
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0)
    await expect(backToTop).toHaveCount(0)
  }

  await page.setViewportSize({ width: 1440, height: 900 })
  for (const route of ['/about', '/transparency/ordinances', '/tourism']) {
    await page.goto(route)
    await page.waitForFunction(() => Boolean(
      (document.querySelector('h1') as
        | (HTMLElement & { __vueParentComponent?: unknown })
        | null)?.__vueParentComponent
    ))
    const backToTop = page.getByRole('button', { name: 'Scroll to top' })
    await expect(backToTop).toHaveCount(0)
    await page.evaluate(() => window.scrollTo(0, 800))
    await expect(backToTop).toBeVisible()
    await backToTop.click()
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0)
  }
})

test('About page provides linked municipal tabs', async ({ page }) => {
  await page.goto('/')
  const headerNavigation = page.locator('header nav').first()
  const aboutLink = headerNavigation.getByRole('link', { name: 'About', exact: true })
  await expect(aboutLink).toHaveAttribute('href', '/about')
  await aboutLink.click()

  const tabs = page.getByRole('navigation', { name: 'About Consolacion sections' })
  const tabRoutes = [
    ['Citizen\'s Charter', '/about'],
    ['Office of the Mayor', '/about/mayor'],
    ['Office of the Vice Mayor', '/about/vice-mayor'],
    ['Municipal Officials', '/about/officials'],
    ['Office Directory', '/about/office-directory'],
    ['Government Actions', '/about/actions']
  ] as const

  for (const [label, route] of tabRoutes) {
    await expect(tabs.getByRole('link', { name: label, exact: true })).toHaveAttribute('href', route)
  }
  await expect(tabs.getByRole('link', { name: 'Citizen\'s Charter' })).toHaveAttribute('aria-current', 'page')
  await expect(page.getByRole('heading', { name: 'About Consolacion' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Vision' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Mission' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Mandate' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Objectives' })).toBeVisible()

  await tabs.getByRole('link', { name: 'Office of the Mayor' }).click()
  await expect(page.getByRole('heading', { name: 'Office of the Mayor' })).toBeVisible()
  await expect(page.getByText('Municipal Hall, Fourth floor')).toBeVisible()
  await expect(page.getByText('239-2908')).toBeVisible()

  await tabs.getByRole('link', { name: 'Office of the Vice Mayor' }).click()
  await expect(page.getByRole('heading', { name: 'Office of the Vice Mayor' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'A Message from the Vice Mayor' })).toBeVisible()
  await expect(page.getByText('239-2908')).toBeVisible()

  await tabs.getByRole('link', { name: 'Municipal Officials' }).click()
  await expect(page.getByRole('heading', { name: 'Municipal Officials' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Sangguniang Bayan Members' })).toBeVisible()
  await expect(page.getByText('Hon. Joannes P. Alegado, MD')).toBeVisible()
})

test('About has separate Citizen\'s Charter and Office Directory pages', async ({ page }) => {
  await page.goto('/about')
  await expect(page.getByRole('heading', { name: 'About Consolacion' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Vision' })).toHaveCount(1)
  await expect(page.getByRole('heading', { name: 'Mission' })).toHaveCount(1)
  await expect(page.getByRole('heading', { name: 'Mandate' })).toHaveCount(1)
  await expect(page.getByRole('heading', { name: 'Objectives' })).toHaveCount(1)
  await expect(page.getByRole('heading', { name: 'Development goal' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Service pledge' })).toBeVisible()

  await page.goto('/about/office-directory')
  await expect(page.getByRole('heading', { name: 'Office directory' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Police Station' })).toBeVisible()
  await expect(
    page.locator('#main-content').getByRole('link', { name: 'info@consolacion.gov.ph' })
  ).toHaveAttribute('href', 'mailto:info@consolacion.gov.ph')
})

test('Services is absent from the header and Transparency categories remain available', async ({ page }) => {
  await page.goto('/')
  const navigation = page.locator('header nav').first()
  const services = navigation.getByRole('link', { name: 'Services', exact: true })
  const transparency = navigation.getByRole('link', { name: 'Transparency', exact: true })

  await expect(services).toHaveCount(0)
  await expect(navigation.getByRole('button', { name: 'Services', exact: true })).toHaveCount(0)
  await expect(transparency).toHaveAttribute('href', '/transparency')
  await transparency.click()
  await expect(page).toHaveURL(/\/transparency$/)
  await expect(page.getByRole('heading', { name: 'Transparency Portal' })).toBeVisible()

  const recordNavigation = page.getByRole('navigation', { name: 'Public record categories' })
  const transparencyLinks = [
    ['Ordinances', '/transparency/ordinances'],
    ['Resolutions', '/transparency/resolutions'],
    ['Executive Orders', '/transparency/executive-orders'],
    ['Memoranda', '/transparency/memorandums'],
    ['Full Disclosure', '/transparency/full-disclosure'],
    ['Bids and Awards', '/transparency/bids-awards'],
    ['Forms', '/transparency/forms']
  ] as const
  for (const [label, to] of transparencyLinks) {
    await expect(recordNavigation.getByRole('link', { name: label, exact: true })).toHaveAttribute('href', to)
  }
})

test('header and footer share navigation destinations', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.goto('/')
  await page.waitForFunction(() => Boolean(
    (document.querySelector('h1') as
      | (HTMLElement & { __vueParentComponent?: unknown })
      | null)?.__vueParentComponent
  ))

  const header = page.locator('header nav').first()
  const footer = page.locator('footer')
  await header.getByRole('link', { name: 'Transparency', exact: true }).hover()
  await expect(header.getByRole('link', { name: /^Ordinances/ })).toBeVisible()

  const sharedLinks = [
    ['About', 'About Consolacion'],
    ['News', 'News and Announcements'],
    ['Transparency', 'Transparency Portal'],
    ['Tourism', 'Tourism'],
    ['Ordinances', 'Ordinances and Resolutions'],
    ['Bids and Awards', 'Bids and Awards'],
    ['Downloadable Forms', 'Forms and Applications']
  ] as const

  for (const [headerLabel, footerLabel] of sharedLinks) {
    const href = await header.getByRole('link', { name: headerLabel }).getAttribute('href')
    expect(href).toBeTruthy()
    await expect(footer.getByRole('link', { name: footerLabel, exact: true })).toHaveAttribute('href', href!)
  }

  const homeHref = await page.locator('header [data-slot="title"]').getAttribute('href')
  await expect(footer.getByRole('link', { name: 'Municipality of Consolacion' })).toHaveAttribute('href', homeHref!)
  const loginHref = await footer.getByRole('link', { name: 'Staff sign in' }).getAttribute('href')
  await expect(page.getByRole('link', { name: 'Staff sign in' }).first()).toHaveAttribute('href', loginHref!)

  await page.setViewportSize({ width: 390, height: 844 })
  await page.getByRole('button', { name: 'Open menu' }).click()
  const mobileMenu = page.getByRole('dialog')
  await expect(mobileMenu).toBeVisible()
  await expect(mobileMenu.getByRole('link', { name: 'Staff sign in' })).toHaveAttribute('href', loginHref!)
})

test('header provides Home and News links on desktop and mobile', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.goto('/about')

  const desktopNavigation = page.locator('header nav').first()
  const homeLink = desktopNavigation.getByRole('link', { name: 'Home', exact: true })
  const newsLink = desktopNavigation.getByRole('link', { name: 'News', exact: true })
  await expect(homeLink).toHaveAttribute('href', '/')
  await expect(newsLink).toHaveAttribute('href', '/news')

  await newsLink.click()
  await expect(page).toHaveURL(/\/news$/)
  await expect(page.getByRole('heading', { name: 'News and announcements' })).toBeVisible()

  await page.setViewportSize({ width: 390, height: 844 })
  await page.waitForFunction(() => Boolean(
    (document.querySelector('h1') as
      | (HTMLElement & { __vueParentComponent?: unknown })
      | null)?.__vueParentComponent
  ))
  const openMenuButton = page.getByRole('button', { name: 'Open menu' })
  await expect(openMenuButton).toBeVisible()
  await openMenuButton.click()
  const mobileMenu = page.getByRole('dialog')
  await expect(mobileMenu).toBeVisible()
  await expect(mobileMenu.getByRole('link', { name: 'Home', exact: true })).toHaveAttribute('href', '/')
  await expect(mobileMenu.getByRole('link', { name: 'News', exact: true })).toHaveAttribute('href', '/news')
})

test('public navigation links share the Transparency tab font size', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.goto('/transparency')

  const transparencyTabs = page.getByRole('navigation', { name: 'Public record categories' })
  await expect(transparencyTabs.getByRole('link', { name: 'Overview', exact: true })).toHaveCSS('font-size', '14px')
  await expect(page.locator('header nav').first().getByRole('link', { name: 'About', exact: true })).toHaveCSS('font-size', '14px')

  await page.goto('/about')
  const aboutTabs = page.getByRole('navigation', { name: 'About Consolacion sections' })
  await expect(aboutTabs.getByRole('link', { name: 'Office of the Mayor', exact: true })).toHaveCSS('font-size', '14px')

  await page.setViewportSize({ width: 390, height: 844 })
  await page.waitForFunction(() => Boolean(
    (document.querySelector('h1') as
      | (HTMLElement & { __vueParentComponent?: unknown })
      | null)?.__vueParentComponent
  ))
  await page.getByRole('button', { name: 'Open menu' }).click()
  await expect(page.getByRole('link', { name: 'About', exact: true })).toHaveCSS('font-size', '14px')
  await expect(page.getByRole('link', { name: 'Staff sign in' }).last()).toHaveCSS('font-size', '14px')
})

test('public section navigation marks the current page and detail category', async ({ page }) => {
  const routes = [
    ['/about', 'About Consolacion sections', 'Citizen\'s Charter'],
    ['/about/mayor', 'About Consolacion sections', 'Office of the Mayor'],
    ['/about/vice-mayor', 'About Consolacion sections', 'Office of the Vice Mayor'],
    ['/about/officials', 'About Consolacion sections', 'Municipal Officials'],
    ['/about/office-directory', 'About Consolacion sections', 'Office Directory'],
    ['/about/actions', 'About Consolacion sections', 'Government Actions'],
    ['/about/actions/clup-2024-2033-adoption', 'About Consolacion sections', 'Government Actions'],
    ['/transparency', 'Public record categories', 'Overview'],
    ['/transparency/ordinances', 'Public record categories', 'Ordinances'],
    ['/transparency/resolutions', 'Public record categories', 'Resolutions'],
    ['/transparency/executive-orders', 'Public record categories', 'Executive Orders'],
    ['/transparency/memorandums', 'Public record categories', 'Memoranda'],
    ['/transparency/full-disclosure', 'Public record categories', 'Full Disclosure'],
    ['/transparency/bids-awards', 'Public record categories', 'Bids and Awards'],
    ['/transparency/forms', 'Public record categories', 'Forms'],
    ['/transparency/document/ordinance-35-2024?kind=ordinance', 'Public record categories', 'Ordinances'],
    ['/transparency/document/resolution-99-2024?kind=resolution', 'Public record categories', 'Resolutions']
  ] as const

  for (const [path, navigation, label] of routes) {
    await page.goto(path)
    const current = page.getByRole('navigation', { name: navigation }).locator('a[aria-current="page"]')
    await expect(current).toHaveCount(1)
    await expect(current).toHaveText(label)
    const indicator = await current.evaluate((element) => {
      const style = getComputedStyle(element, '::after')
      const viewport = element.closest('nav')!.parentElement!.getBoundingClientRect()
      const bottom = element.getBoundingClientRect().bottom - Number.parseFloat(style.bottom)
      return { visible: bottom > viewport.top && bottom <= viewport.bottom + 0.5, background: style.backgroundColor }
    })
    expect(indicator.visible).toBeTruthy()
    expect(indicator.background).not.toBe('rgba(0, 0, 0, 0)')
  }
})

test('mobile navigation works without horizontal overflow', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('/')
  await page.waitForFunction(() => Boolean(
    (document.querySelector('h1') as
      | (HTMLElement & { __vueParentComponent?: unknown })
      | null)?.__vueParentComponent
  ))

  await page.getByRole('button', { name: 'Open menu' }).click()
  await expect(page.getByRole('link', { name: 'About', exact: true })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Tourism', exact: true })).toBeVisible()
  await page.getByRole('link', { name: 'About', exact: true }).click()
  const aboutTabs = page.getByRole('navigation', { name: 'About Consolacion sections' })
  await expect(aboutTabs).toBeVisible()
  expect(await aboutTabs.locator('..').evaluate(element => element.scrollWidth > element.clientWidth)).toBeTruthy()
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)
  ).toBeTruthy()

  await page.goto('/transparency')
  const transparencyTabs = page.getByRole('navigation', { name: 'Public record categories' })
  expect(await transparencyTabs.locator('..').evaluate(element => element.scrollWidth > element.clientWidth)).toBeTruthy()
  await transparencyTabs.getByRole('link', { name: 'Forms', exact: true }).click()
  await expect(page).toHaveURL(/\/transparency\/forms$/)
  await expect(transparencyTabs.getByRole('link', { name: 'Forms', exact: true })).toHaveAttribute('aria-current', 'page')
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBeTruthy()
})

test('static ordinance archive filters titles and years locally', async ({ page }) => {
  await page.goto('/transparency/ordinances')
  await page.waitForFunction(() => Boolean(
    (document.querySelector('h1') as
      | (HTMLElement & { __vueParentComponent?: unknown })
      | null)?.__vueParentComponent
  ))

  const titleLink = page.getByRole('link', { name: /ORDINANCE NO\. 35/ })
  const fullTitle = await titleLink.innerText()
  await expect(titleLink).toHaveCSS('text-overflow', 'ellipsis')
  await expect.poll(() => titleLink.evaluate(element => element.scrollWidth > element.clientWidth)).toBeTruthy()
  await titleLink.hover()
  const titleTooltip = page.locator('[data-slot="content"]').filter({ hasText: fullTitle }).last()
  await expect(titleTooltip).toBeVisible()
  await expect(titleTooltip).toContainText(fullTitle)

  const searchInput = page.getByRole('textbox', { name: 'Search public records' })
  await searchInput.fill('youth welfare')
  await expect(page.getByRole('link', { name: /ORDINANCE NO\. 35/ })).toBeVisible()
  await page.getByRole('button', { name: 'Filter by publication year' }).click()
  await page.getByRole('option', { name: '2024' }).click()
  await page.getByRole('link', { name: /Providing a comprehensive Youth Welfare/i }).click()
  await expect(page.getByRole('dialog')).toContainText('ORDINANCE NO. 35')
  await expect(page.getByRole('dialog')).toContainText('PDF preview unavailable')
})
