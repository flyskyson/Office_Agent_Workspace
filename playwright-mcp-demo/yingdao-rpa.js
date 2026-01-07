const { chromium } = require('playwright');

(async () => {
  let browser;

  try {
    console.log('🚀 正在启动浏览器...');

    // 启动浏览器
    browser = await chromium.launch({
      headless: false,
      args: ['--start-maximized']
    });

    console.log('✅ 浏览器启动成功');

    const context = await browser.newContext({
      viewport: null
    });

    const page = await context.newPage();

    // 影刀RPA官网
    console.log('\n🌐 正在访问影刀RPA官网...');
    await page.goto('https://www.yingdao.com/', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    const title = await page.title();
    console.log('📌 页面标题:', title);

    // 截图保存官网首页
    await page.screenshot({
      path: 'yingdao-homepage.png',
      fullPage: true
    });
    console.log('📸 官网截图已保存: yingdao-homepage.png');

    // 等待 3 秒
    await page.waitForTimeout(3000);

    // 访问训练课程页面
    console.log('\n🎓 正在访问影刀RPA训练课程页面...');
    await page.goto('https://rpa-client.yingdao.com/course', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    const courseTitle = await page.title();
    console.log('📌 课程页面标题:', courseTitle);

    // 截图保存课程页面
    await page.screenshot({
      path: 'yingdao-courses.png',
      fullPage: true
    });
    console.log('📸 课程页面截图已保存: yingdao-courses.png');

    // 尝试获取课程信息
    console.log('\n📚 正在分析课程页面...');

    try {
      // 等待页面加载
      await page.waitForTimeout(2000);

      // 获取页面主要文本内容
      const pageText = await page.textContent('body');

      // 查找课程相关关键词
      const keywords = ['初级课程', '中级课程', '高级课程', '案例课程', '视频教程'];
      const foundKeywords = keywords.filter(keyword => pageText.includes(keyword));

      if (foundKeywords.length > 0) {
        console.log('✅ 找到以下课程类型:');
        foundKeywords.forEach(keyword => {
          console.log(`   • ${keyword}`);
        });
      }

    } catch (error) {
      console.log('⚠️ 课程信息获取失败:', error.message);
    }

    // 保持浏览器打开 15 秒供查看
    console.log('\n⏳ 浏览器将在 15 秒后关闭...');
    await page.waitForTimeout(15000);

    console.log('\n✅ 任务完成!');
    console.log('\n📋 访问的页面:');
    console.log('   1. 影刀RPA官网: https://www.yingdao.com/');
    console.log('   2. 训练课程页面: https://rpa-client.yingdao.com/course');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('\n🔒 浏览器已关闭');
    }
  }
})();
