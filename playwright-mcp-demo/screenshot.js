const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    // 示例: 截图网站
    await page.goto('https://example.com');
    await page.screenshot({ path: 'example-screenshot.png', fullPage: true });
    console.log('✅ 截图已保存: example-screenshot.png');

    await page.waitForTimeout(3000);
  } catch (error) {
    console.error('❌ 错误:', error.message);
  } finally {
    await browser.close();
  }
})();
