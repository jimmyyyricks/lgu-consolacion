import { expect, test } from '@playwright/test'

test('staff login is clearly labeled and does not appear as public content', async ({ page }) => {
  const response = await page.goto('/login')
  expect(response?.ok()).toBeTruthy()
  await expect(page.getByRole('heading', { name: 'Staff sign in' })).toBeVisible()
  await expect(page.getByLabel('Username')).toBeVisible()
  await expect(page.getByLabel('Password')).toBeVisible()
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex, nofollow')
})
