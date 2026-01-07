const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    console.log('📝 正在打开表单页面...');
    await page.goto('https://www.selenium.dev/selenium/web/web-form.html');

    // 等待页面加载
    await page.waitForLoadState('networkidle');

    // 验证页面标题
    const title = await page.title();
    console.log('📌 页面标题:', title);
    console.assert(title === 'Web form', '❌ 页面标题不正确!');

    // 填写文本输入
    console.log('\n✍️ 正在填写表单...');
    await page.fill('#my-text-id', 'Playwright 测试');
    console.log('✅ Text input: Playwright 测试');

    // 填写密码
    await page.fill('input[name="my-password"]', 'password123');
    console.log('✅ Password: ********');

    // 选择下拉菜单
    await page.selectOption('select[name="my-select"]', '2');
    console.log('✅ Dropdown: Two');

    // 输入日期
    await page.fill('input[name="my-date"]', '2025-01-06');
    console.log('✅ Date: 2025-01-06');

    // 截图
    await page.screenshot({ path: 'form-filled.png' });
    console.log('📸 截图已保存: form-filled.png');

    // 点击提交按钮
    console.log('\n🚀 正在提交表单...');
    await Promise.all([
      page.waitForURL('**/web-form.html'),
      page.click('button[type="submit"]')
    ]);

    // 等待提交完成
    await page.waitForTimeout(2000);

    // 验证提交结果
    const message = await page.textContent('#message');
    console.log('\n✨ 提交结果:', message);

    if (message === 'Received!') {
      console.log('✅ 表单提交成功!');
    } else {
      console.log('❌ 表单提交失败!');
    }

    await page.waitForTimeout(3000);
  } catch (error) {
    console.error('❌ 错误:', error.message);
  } finally {
    await browser.close();
  }
})();
