import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.QA_BASE_URL || process.env.BASE_URL;
if (!baseURL) throw new Error('Set QA_BASE_URL before running visual regression.');

export default defineConfig({
  testDir: './tests/e2e',
  testMatch: 'visual-baseline.spec.ts',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: 0,
  timeout: 45_000,
  expect: {
    timeout: 10_000,
    toHaveScreenshot: { animations: 'disabled', caret: 'hide', maxDiffPixelRatio: 0.005 },
  },
  reporter: [['list'], ['html', { outputFolder: 'visual-report', open: 'never' }],
             ['json', { outputFile: 'release-evidence/visual-report.json' }]],
  outputDir: 'visual-test-results',
  snapshotPathTemplate: '{testDir}/__screenshots__/{arg}-{projectName}{ext}',
  use: { baseURL, trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
