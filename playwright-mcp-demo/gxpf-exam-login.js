const { chromium } = require('playwright');

(async () => {
  let browser;

  try {
    console.log('🚀 正在启动浏览器...');

    browser = await chromium.launch({
      headless: false,
      args: ['--start-maximized']
    });

    const context = await browser.newContext({
      viewport: null
    });

    const page = await context.newPage();

    console.log('🌐 正在访问广西考试页面...');
    console.log('URL: https://gxpf.sft.gxzf.gov.cn/portal/exam/home\n');

    await page.goto('https://gxpf.sft.gxzf.gov.cn/portal/exam/home', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    const title = await page.title();
    console.log('📌 页面标题:', title);

    // 等待页面加载
    await page.waitForTimeout(3000);

    // 截图保存登录页面
    await page.screenshot({
      path: 'gxpf-exam-login-page.png',
      fullPage: true
    });
    console.log('📸 登录页面截图已保存: gxpf-exam-login-page.png');

    // 尝试分析页面结构
    console.log('\n📊 正在分析页面结构...\n');

    try {
      // 查找用户名输入框
      const usernameInput = await page.locator('input[type="text"], input[name*="user"], input[id*="user"], input[placeholder*="用户"]').first();
      if (await usernameInput.isVisible()) {
        console.log('✅ 找到用户名输入框');
      }

      // 查找密码输入框
      const passwordInput = await page.locator('input[type="password"]').first();
      if (await passwordInput.isVisible()) {
        console.log('✅ 找到密码输入框');
      }

      // 查找验证码
      const captcha = await page.locator('img[src*="captcha"], img[src*="code"], img[alt*="验证"]').first();
      if (await captcha.isVisible()) {
        console.log('✅ 找到验证码图片');

        // 截图验证码
        await captcha.screenshot({
          path: 'gxpf-captcha.png'
        });
        console.log('📸 验证码截图已保存: gxpf-captcha.png');
      }

      // 查找登录按钮
      const loginButton = await page.locator('button[type="submit"], button:has-text("登录"), input[type="submit"]').first();
      if (await loginButton.isVisible()) {
        const buttonText = await loginButton.textContent();
        console.log('✅ 找到登录按钮:', buttonText);
      }

    } catch (error) {
      console.log('⚠️ 页面结构分析失败:', error.message);
    }

    // 获取页面文本信息
    const pageText = await page.textContent('body');

    console.log('\n📝 页面关键词信息:');
    if (pageText.includes('登录')) console.log('   • 包含"登录"相关内容');
    if (pageText.includes('考试')) console.log('   • 包含"考试"相关内容');
    if (pageText.includes('成绩')) console.log('   • 包含"成绩"相关内容');
    if (pageText.includes('验证码')) console.log('   • 包含"验证码"相关内容');

    console.log('\n⏳ 浏览器将保持打开 60 秒,供你查看页面...');
    console.log('💡 提示: 如果需要登录,请手动登录后告诉我下一步操作');
    await page.waitForTimeout(60000);

    console.log('\n✅ 任务完成!');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('\n🔒 浏览器已关闭');
    }
  }
})();
