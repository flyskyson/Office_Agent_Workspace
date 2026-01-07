const { chromium } = require('playwright');

// 淘宝搜索链接生成
const products = [
  { name: '联想小新Pro 14 2024', keyword: '联想小新Pro14 2024 笔记本' },
  { name: '华硕无畏Pro 15', keyword: '华硕无畏Pro15 笔记本' },
  { name: '荣耀MagicBook 14 Pro', keyword: '荣耀MagicBook 14 Pro' },
  { name: '惠普战66 六代', keyword: '惠普战66 笔记本' },
  { name: '机械革命无界14 Pro', keyword: '机械革命无界14 Pro' },
  { name: 'ThinkBook 14+', keyword: 'ThinkBook 14+ 笔记本' },
  { name: 'RedmiBook Pro 14', keyword: 'RedmiBook Pro 14 笔记本' }
];

(async () => {
  let browser;

  try {
    console.log('🚀 正在启动浏览器...\n');

    browser = await chromium.launch({
      headless: false,
      args: ['--start-maximized']
    });

    const context = await browser.newContext({
      viewport: null
    });

    const page = await context.newPage();

    console.log('📋 笔记本电脑购买清单生成器\n');
    console.log('='.repeat(80) + '\n');

    // 生成淘宝搜索链接
    console.log('🔗 淘宝搜索链接:\n\n');

    const shoppingLinks = [];

    products.forEach((product, index) => {
      const searchUrl = `https://s.taobao.com/search?q=${encodeURIComponent(product.keyword)}`;
      shoppingLinks.push({
        序号: index + 1,
        产品名称: product.name,
        搜索关键词: product.keyword,
        淘宝链接: searchUrl
      });

      console.log(`${index + 1}. ${product.name}`);
      console.log(`   搜索关键词: ${product.keyword}`);
      console.log(`   淘宝链接: ${searchUrl}\n`);
    });

    console.log('='.repeat(80));

    // 访问第一个推荐产品的搜索页面
    console.log('\n🌐 正在打开淘宝搜索页面...');
    console.log('产品: 联想小新Pro 14 (高性价比推荐)\n');

    await page.goto('https://s.taobao.com/search?q=' + encodeURIComponent('联想小新Pro14 2024 笔记本'), {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    console.log('✅ 已打开淘宝搜索页面');
    console.log('📌 页面标题:', await page.title());

    // 等待并滚动
    await page.waitForTimeout(3000);

    console.log('\n📜 正在滚动加载更多商品...');

    for (let i = 0; i < 3; i++) {
      await page.evaluate(() => {
        window.scrollBy(0, window.innerHeight);
      });
      await page.waitForTimeout(2000);
    }

    // 截图
    await page.screenshot({
      path: 'taobao-laptop-recommendation.png',
      fullPage: true
    });

    console.log('📸 搜索结果截图已保存: taobao-laptop-recommendation.png');

    console.log('\n⏳ 浏览器将在 30 秒后关闭,您可以浏览商品...');
    await page.waitForTimeout(30000);

    console.log('\n✅ 任务完成!');
    console.log('\n📄 已生成以下文件:');
    console.log('   - laptop-recommendations.md (详细推荐清单)');
    console.log('   - taobao-laptop-recommendation.png (淘宝搜索截图)');
    console.log('   - laptop-shopping-guide.js (本脚本)');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('\n🔒 浏览器已关闭');
    }
  }
})();
