const { chromium } = require('playwright');

(async () => {
  // 使用系统已安装的 Chrome 浏览器
  const browser = await chromium.launch({
    channel: 'chrome', // 使用系统的 Chrome
    headless: false
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    console.log('正在打开网页...');

    // 打开网页
    await page.goto('https://example.com');

    // 获取页面标题
    const title = await page.title();
    console.log('页面标题:', title);

    // 获取主要内容
    const content = await page.textContent('body');
    console.log('页面内容:', content.substring(0, 200) + '...');

    // 截图
    await page.screenshot({ path: 'screenshot.png' });
    console.log('截图已保存为 screenshot.png');

    // 等待 5 秒以便查看
    await page.waitForTimeout(5000);

  } catch (error) {
    console.error('发生错误:', error);
  } finally {
    // 关闭浏览器
    await browser.close();
    console.log('浏览器已关闭');
  }
})();
