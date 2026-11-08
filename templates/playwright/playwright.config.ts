import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.QA_BASE_URL || process.env.BASE_URL;
if (!baseURL) throw new Error('Set QA_BASE_URL to the running site origin before browser QA.');
const parsed = new URL(baseURL);
if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('QA_BASE_URL must use HTTP or HTTPS.');

export default defineConfig({
  testDir: './tests/e2e',
  testMatch: 'site-quality.spec.ts',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 3 : undefined,
  timeout: 30_000,
  expect: { timeout: 7_000 },
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'release-evidence/playwright-report.json' }],
  ],
  outputDir: 'test-results',
  use: {
    baseURL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10_000,
    navigationTimeout: 15_000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
