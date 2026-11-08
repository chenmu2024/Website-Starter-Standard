import { test, expect } from '@playwright/test';

async function findUnnamedControls(page: import('@playwright/test').Page): Promise<string[]> {
  return page.evaluate(() => {
    return Array.from(document.querySelectorAll(
      'button, input:not([type="hidden"]), select, textarea, a[href]'
    )).filter(element => {
      const el = element as HTMLElement;
      if (el.closest('[hidden], [inert], [aria-hidden="true"]') || el.getClientRects().length === 0) {
        return false;
      }
      let ancestor: HTMLElement | null = el;
      while (ancestor) {
        const style = getComputedStyle(ancestor);
        if (style.display === 'none' || style.visibility === 'hidden' ||
            style.visibility === 'collapse' || style.contentVisibility === 'hidden') {
          return false;
        }
        ancestor = ancestor.parentElement;
      }
      const labelledBy = (el.getAttribute('aria-labelledby') || '').split(/\s+/)
        .filter(Boolean)
        .map(id => document.getElementById(id)?.textContent?.trim() || '')
        .filter(Boolean).join(' ');
      const nativeLabels = ('labels' in el
        ? Array.from((el as HTMLInputElement).labels || [])
            .map(label => label.textContent?.trim() || '').filter(Boolean).join(' ')
        : '');
      const input = el instanceof HTMLInputElement ? el : null;
      const valueName = input && ['button', 'submit', 'reset'].includes(input.type)
        ? input.value.trim() : '';
      const imageInputAlt = input?.type === 'image' ? input.alt.trim() : '';
      const supportsContentName = el instanceof HTMLButtonElement || el instanceof HTMLAnchorElement;
      const contentName = supportsContentName ? el.innerText?.trim() || '' : '';
      const imageAlt = supportsContentName ? el.querySelector('img')?.getAttribute('alt') || '' : '';
      const svgTitle = supportsContentName ? el.querySelector('svg title')?.textContent?.trim() || '' : '';
      const labelled = el.getAttribute('aria-label') || labelledBy ||
        el.getAttribute('title') || nativeLabels ||
        valueName || imageInputAlt || contentName || imageAlt || svgTitle;
      return !labelled;
    }).map(element => element.tagName.toLowerCase() + '.' + (element as HTMLElement).className);
  });
}

const routes = JSON.parse(process.env.QA_ROUTES_JSON || '[]') as string[];
if (!Array.isArray(routes) || routes.length === 0 ||
    routes.some(route => typeof route !== 'string' || !route.startsWith('/') || route.startsWith('//'))) {
  throw new Error('QA_ROUTES_JSON must be a nonempty JSON array of same-site absolute paths.');
}

const viewports = [
  { name: 'mobile-360', width: 360, height: 800 },
  { name: 'mobile-390', width: 390, height: 844 },
  { name: 'tablet-768', width: 768, height: 1024 },
  { name: 'laptop-1024', width: 1024, height: 768 },
  { name: 'desktop-1440', width: 1440, height: 900 },
];

for (const route of routes) {
  for (const viewport of viewports) {
    test(route + ' · ' + viewport.name + ' · layout and runtime', async ({ page }, testInfo) => {
      const uncaught: string[] = [];
      page.on('pageerror', error => uncaught.push(error.message));
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      const response = await page.goto(route, { waitUntil: 'domcontentloaded' });
      expect(response, 'No document response for ' + route).not.toBeNull();
      expect(response!.status(), 'HTTP status for ' + route).toBeLessThan(400);
      await page.waitForLoadState('load', { timeout: 8_000 }).catch(() => undefined);
      await page.evaluate(async () => { await document.fonts.ready; });

      await expect(page).toHaveTitle(/\S/);
      await expect(page.locator('html')).toHaveAttribute('lang', /\S+/);
      await expect(page.locator('meta[name="viewport"]')).toHaveCount(1);

      const layout = await page.evaluate(() => {
        const root = document.documentElement;
        const visibleBrokenImages = Array.from(document.images).filter(image => {
          const rect = image.getBoundingClientRect();
          const visible = rect.width > 0 && rect.height > 0 &&
            rect.bottom > 0 && rect.top < window.innerHeight;
          return visible && image.complete && image.naturalWidth === 0;
        }).map(image => image.currentSrc || image.src);
        return {
          width: window.innerWidth,
          documentWidth: Math.max(root.scrollWidth, document.body?.scrollWidth || 0),
          visibleBrokenImages,
        };
      });
      expect(layout.documentWidth, 'Horizontal overflow: ' + JSON.stringify(layout))
        .toBeLessThanOrEqual(layout.width + 1);
      expect(layout.visibleBrokenImages, 'Visible images must load').toEqual([]);
      const unnamedControls = await findUnnamedControls(page);
      expect(unnamedControls, 'Interactive controls need accessible names').toEqual([]);
      expect(uncaught, 'Uncaught browser runtime errors').toEqual([]);

      if (process.env.QA_PRIMARY_TASK_SELECTOR) {
        await expect(page.locator(process.env.QA_PRIMARY_TASK_SELECTOR)).toBeVisible();
      }
      if (process.env.QA_CAPTURE_SCREENSHOTS === '1') {
        await page.screenshot({
          path: testInfo.outputPath(testInfo.project.name + '-' + viewport.name + '.png'),
          fullPage: true,
          animations: 'disabled',
        });
      }
    });
  }
}

test('accessible-name check does not treat option text or textarea contents as labels', async ({ page }) => {
  await page.setContent(`<!doctype html>
      <html lang="en"><body>
        <select class="unlabelled-select"><option>Choose a size</option></select>
        <textarea class="unlabelled-textarea">Default notes</textarea>
        <label for="named-select">Named size</label>
        <select id="named-select"><option>Small</option></select>
      </body></html>`);
  const unnamed = await findUnnamedControls(page);
  expect(unnamed).toEqual([
    'select.unlabelled-select',
    'textarea.unlabelled-textarea',
  ]);
});
