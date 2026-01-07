const { chromium } = require('playwright');

(async () => {
  let browser;

  try {
    console.log('🚀 正在启动 Chrome 浏览器...');

    // 使用系统已安装的 Chrome
    browser = await chromium.launch({
      channel: 'chrome',
      headless: false,
      args: ['--start-maximized']
    });

    console.log('✅ 浏览器启动成功');

    const context = await browser.newContext({
      viewport: null // 使用最大化的窗口
    });

    const page = await context.newPage();

    console.log('🌐 正在访问 example.com...');
    await page.goto('https://example.com', { waitUntil: 'networkidle' });

    // 获取页面标题
    const title = await page.title();
    console.log('📌 页面标题:', title);

    // 获取标题文本
    const heading = await page.textContent('h1');
    console.log('📝 页面标题:', heading);

    // 获取段落内容
    const paragraph = await page.textContent('p');
    console.log('📄 页面内容:', paragraph);

    // 截图
    await page.screenshot({ path: 'example-screenshot.png', fullPage: true });
    console.log('📸 截图已保存: example-screenshot.png');

    // 保持浏览器打开 10 秒
    console.log('⏳ 浏览器将在 10 秒后关闭...');
    await page.waitForTimeout(10000);

    console.log('✅ 测试成功!');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
    console.error(error.stack);
  } finally {
    if (browser) {
      await browser.close();
      console.log('🔒 浏览器已关闭');
    }
  }
})();
