const { chromium } = require('playwright');
const fs = require('fs');

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

    console.log('🌐 正在访问广西普法网...\n');

    await page.goto('https://gxpf.sft.gxzf.gov.cn/portal/exam/home', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    console.log('✅ 页面已打开');
    console.log('⏳ 等待 30 秒供你登录...\n');

    // 等待用户登录
    await page.waitForTimeout(30000);

    console.log('🔍 正在检查页面状态...\n');

    const currentUrl = page.url();
    console.log('当前 URL:', currentUrl);
    console.log('页面标题:', await page.title());

    // 截图当前页面
    await page.screenshot({
      path: 'gxpf-current-page.png',
      fullPage: true
    });
    console.log('📸 当前页面截图已保存: gxpf-current-page.png\n');

    // 保存页面HTML
    fs.writeFileSync('gxpf-current-page.html', await page.content(), 'utf-8');
    console.log('💾 页面HTML已保存: gxpf-current-page.html\n');

    console.log('📊 正在分析页面内容...\n');

    // 获取页面文本
    const pageText = await page.textContent('body');

    // 查找关键词
    const keywords = ['成绩', '分数', '考试', '及格', '优秀', '满分'];
    const foundKeywords = keywords.filter(kw => pageText.includes(kw));

    if (foundKeywords.length > 0) {
      console.log('✅ 找到以下关键词:');
      foundKeywords.forEach(kw => console.log(`   • ${kw}`));
      console.log('');
    }

    // 查找表格
    console.log('📋 正在查找表格数据...\n');
    const tables = await page.locator('table').all();
    console.log(`找到 ${tables.length} 个表格\n`);

    const scores = [];

    for (let i = 0; i < tables.length; i++) {
      const table = tables[i];
      const rows = await table.locator('tr').all();

      if (rows.length > 0) {
        console.log(`=== 表格 ${i + 1} (${rows.length} 行) ===`);

        for (let j = 0; j < Math.min(rows.length, 20); j++) {
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
            scores.push({
              表格: i + 1,
              行号: j + 1,
              数据: cellTexts
            });
          }
        }
        console.log('');
      }
    }

    // 查找列表项
    console.log('📋 正在查找列表数据...\n');
    const lists = await page.locator('ul, ol, li').all();
    console.log(`找到 ${lists.length} 个列表元素\n`);

    // 保存数据
    if (scores.length > 0) {
      fs.writeFileSync(
        'exam-scores-extracted.json',
        JSON.stringify(scores, null, 2),
        'utf-8'
      );
      console.log('✅ 数据已保存到: exam-scores-extracted.json\n');

      // 生成 Markdown 报告
      let markdown = '# 广西普法考试成绩单\n\n';
      markdown += `**查询时间**: ${new Date().toLocaleString('zh-CN')}\n`;
      markdown += `**页面URL**: ${currentUrl}\n\n`;
      markdown += '---\n\n';

      scores.forEach((item) => {
        markdown += `### 表格 ${item.表格} - 行 ${item.行号}\n\n`;
        item.数据.forEach((cell, idx) => {
          markdown += `${idx + 1}. ${cell}\n`;
        });
        markdown += '\n';
      });

      fs.writeFileSync('exam-scores-extracted.md', markdown, 'utf-8');
      console.log('📄 报告已保存到: exam-scores-extracted.md\n');
    } else {
      console.log('⚠️ 未找到表格数据\n');

      // 尝试提取所有文本
      console.log('📝 正在提取页面文本内容...\n');
      const allText = await page.textContent('body');

      // 保存文本
      fs.writeFileSync('gxpf-page-text.txt', allText, 'utf-8');
      console.log('💾 页面文本已保存到: gxpf-page-text.txt\n');

      // 查找可能的考试信息
      const lines = allText.split('\n').filter(line => line.trim());
      const relevantLines = lines.filter(line => {
        return line.includes('考试') || line.includes('成绩') || line.includes('分数') ||
               line.match(/\d+分/) || line.match(/\d{4}-\d{2}-\d{2}/);
      });

      if (relevantLines.length > 0) {
        console.log('📋 可能相关的信息:\n');
        relevantLines.slice(0, 20).forEach(line => {
          console.log(`  ${line.trim()}`);
        });

        fs.writeFileSync(
          'gxpf-relevant-info.txt',
          relevantLines.join('\n'),
          'utf-8'
        );
        console.log('\n💾 相关信息已保存到: gxpf-relevant-info.txt\n');
      }
    }

    console.log('⏳ 浏览器将在 60 秒后关闭,你可以查看页面...');
    await page.waitForTimeout(60000);

    console.log('\n✅ 任务完成!');
    console.log('\n📁 生成的文件:');
    console.log('   - gxpf-current-page.png (页面截图)');
    console.log('   - gxpf-current-page.html (页面HTML)');
    console.log('   - exam-scores-extracted.json (成绩数据)');
    console.log('   - exam-scores-extracted.md (成绩报告)');
    console.log('   - gxpf-page-text.txt (页面文本)');
    console.log('   - gxpf-relevant-info.txt (相关信息)');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('\n🔒 浏览器已关闭');
    }
  }
})();
