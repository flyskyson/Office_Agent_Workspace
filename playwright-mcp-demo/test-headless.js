const { chromium } = require('playwright');

(async () => {
  let browser;

  try {
    console.log('🚀 正在启动浏览器(headless 模式)...');

    // 尝试使用 headless 模式
    browser = await chromium.launch({
      headless: true
    });

    console.log('✅ 浏览器启动成功');

    const page = await browser.newPage();

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

    console.log('✅ 测试成功!');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('🔒 浏览器已关闭');
    }
  }
})();
