const { chromium } = require('playwright');

(async () => {
  let browser;

  try {
    console.log('🚀 正在启动浏览器...');

    // 启动浏览器 (使用 headless: false 可以看到浏览器窗口)
    browser = await chromium.launch({
      headless: false,
      args: ['--start-maximized']
    });

    console.log('✅ 浏览器启动成功');

    const context = await browser.newContext({
      viewport: null // 使用最大化的窗口
    });

    const page = await context.newPage();

    console.log('🌐 正在访问淘宝首页...');

    // 访问淘宝首页
    await page.goto('https://www.taobao.com', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    // 等待页面加载完成
    await page.waitForLoadState('domcontentloaded');

    console.log('📌 页面标题:', await page.title());

    // 截图保存
    await page.screenshot({
      path: 'taobao-homepage.png',
      fullPage: true
    });
    console.log('📸 截图已保存: taobao-homepage.png');

    // 尝试获取页面主要信息
    try {
      // 搜索框
      const searchBox = await page.locator('#q').first();
      if (await searchBox.isVisible()) {
        console.log('✅ 找到搜索框');

        // 在搜索框中输入文字
        await searchBox.fill('Playwright 自动化');
        console.log('✍️ 已在搜索框输入: Playwright 自动化');

        // 等待 2 秒
        await page.waitForTimeout(2000);

        // 再次截图
        await page.screenshot({ path: 'taobao-search-filled.png' });
        console.log('📸 搜索框截图已保存: taobao-search-filled.png');
      }
    } catch (error) {
      console.log('⚠️ 搜索框未找到或页面结构已变化');
    }

    // 保持浏览器打开 10 秒供查看
    console.log('⏳ 浏览器将在 10 秒后关闭...');
    await page.waitForTimeout(10000);

    console.log('✅ 任务完成!');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('🔒 浏览器已关闭');
    }
  }
})();
