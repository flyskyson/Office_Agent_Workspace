const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;

  try {
    console.log('🚀 广西普法考试成绩查询助手\n');

    browser = await chromium.launch({
      headless: false, // 显示浏览器窗口
      args: ['--start-maximized']
    });

    const context = await browser.newContext({
      viewport: null
    });

    const page = await context.newPage();

    console.log('🌐 正在访问广西普法网...\n');

    await page.goto('https://gxpf.sft.gxzf.gov.cn/portal/exam/home', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    console.log('📌 页面标题:', await page.title());
    console.log('\n' + '='.repeat(80));
    console.log('📋 操作说明:');
    console.log('='.repeat(80));
    console.log('\n✅ 已打开登录页面');
    console.log('⏳ 浏览器将保持打开 120 秒\n');
    console.log('请在浏览器中完成以下操作:');
    console.log('  1. 输入用户名和密码');
    console.log('  2. 输入验证码');
    console.log('  3. 点击"用户登录"按钮');
    console.log('  4. 等待跳转到成绩页面\n');
    console.log('登录成功后,脚本将自动提取成绩信息!\n');
    console.log('='.repeat(80) + '\n');

    // 等待用户手动登录
    await page.waitForTimeout(120000);

    console.log('⏳ 时间到!正在检查登录状态...\n');

    // 检查是否登录成功 (通过URL变化或页面元素)
    const currentUrl = page.url();
    console.log('当前页面:', currentUrl);

    // 尝试查找成绩相关信息
    console.log('\n📊 正在查找成绩信息...\n');

    // 方法1: 查找包含"成绩"的元素
    try {
      const scoreElements = await page.locator(':text-is("成绩"), :text-is("分数"), :text-is("考试")').all();
      console.log(`✅ 找到 ${scoreElements.length} 个包含成绩相关的元素\n`);

      // 获取页面主要内容
      const mainContent = await page.textContent('body');

      // 保存页面HTML用于分析
      fs.writeFileSync('gxpf-page-content.html', await page.content(), 'utf-8');
      console.log('💾 页面HTML已保存到: gxpf-page-content.html\n');

      // 截图保存当前页面
      await page.screenshot({
        path: 'gxpf-exam-result.png',
        fullPage: true
      });
      console.log('📸 成绩页面截图已保存: gxpf-exam-result.png\n');

      // 尝试提取结构化数据
      console.log('📋 正在提取成绩数据...\n');

      const scores = [];

      // 查找表格或列表
      const tables = await page.locator('table').all();
      console.log(`找到 ${tables.length} 个表格\n`);

      for (let i = 0; i < tables.length; i++) {
        const table = tables[i];
        const rows = await table.locator('tr').all();

        if (rows.length > 0) {
          console.log(`表格 ${i + 1}:`);
          for (let j = 0; j < Math.min(rows.length, 10); j++) {
            const row = rows[j];
            const cells = await row.locator('td, th').all();
            const cellTexts = [];

            for (const cell of cells) {
              const text = await cell.textContent();
              if (text.trim()) {
                cellTexts.push(text.trim());
              }
            }

            if (cellTexts.length > 0) {
              console.log(`  ${cellTexts.join(' | ')}`);
              scores.push(cellTexts);
            }
          }
          console.log('');
        }
      }

      // 保存提取的数据
      if (scores.length > 0) {
        fs.writeFileSync(
          'exam-scores.json',
          JSON.stringify(scores, null, 2),
          'utf-8'
        );
        console.log('✅ 成绩数据已保存到: exam-scores.json');

        // 生成 Markdown 报告
        let markdown = '# 广西普法考试成绩单\n\n';
        markdown += `**查询时间**: ${new Date().toLocaleString('zh-CN')}\n\n`;
        markdown += '---\n\n';

        scores.forEach((row, index) => {
          markdown += `## 记录 ${index + 1}\n\n`;
          row.forEach((cell, i) => {
            markdown += `- 数据 ${i + 1}: ${cell}\n`;
          });
          markdown += '\n';
        });

        fs.writeFileSync('exam-scores.md', markdown, 'utf-8');
        console.log('📄 Markdown 报告已保存到: exam-scores.md');
      }

    } catch (error) {
      console.log('⚠️ 数据提取失败:', error.message);
    }

    // 保持浏览器打开供查看
    console.log('\n⏳ 浏览器将在 30 秒后关闭...');
    await page.waitForTimeout(30000);

    console.log('\n✅ 任务完成!');
    console.log('\n📁 生成的文件:');
    console.log('   - gxpf-page-content.html (页面HTML)');
    console.log('   - gxpf-exam-result.png (成绩页面截图)');
    console.log('   - exam-scores.json (成绩数据JSON)');
    console.log('   - exam-scores.md (成绩报告Markdown)');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('\n🔒 浏览器已关闭');
    }
  }
})();
