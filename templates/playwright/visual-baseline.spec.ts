import { test, expect } from '@playwright/test';

const routes = JSON.parse(process.env.QA_VISUAL_ROUTES_JSON || '[]') as string[];
if (!Array.isArray(routes) || routes.length === 0 ||
    routes.some(route => typeof route !== 'string' || !route.startsWith('/') || route.startsWith('//'))) {
  throw new Error('Visual regression requires QA_VISUAL_ROUTES_JSON with approved routes.');
}

const viewports = [
  { name: 'mobile-390', width: 390, height: 844 },
  { name: 'desktop-1440', width: 1440, height: 900 },
];

for (const route of routes) {
  const safe = route === '/' ? 'home' : route.replace(/^\/|\/$/g, '').replaceAll('/', '-');
  for (const viewport of viewports) {
    test(route + ' · ' + viewport.name + ' · reviewed visual baseline', async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.emulateMedia({ reducedMotion: 'reduce' });
      const response = await page.goto(route, { waitUntil: 'domcontentloaded' });
      expect(response?.status()).toBeLessThan(400);
      await page.waitForLoadState('load', { timeout: 8_000 }).catch(() => undefined);
      await page.evaluate(() => document.fonts?.ready);
      await expect(page).toHaveScreenshot(safe + '-' + viewport.name + '.png', {
        fullPage: true,
        animations: 'disabled',
        caret: 'hide',
        maxDiffPixelRatio: Number(process.env.QA_VISUAL_DIFF_RATIO || 0.005),
        mask: [page.locator('[data-visual-mask]')],
      });
    });
  }
}
