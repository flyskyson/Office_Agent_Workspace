const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;

  try {
    console.log('🚀 广西普法网 - 详细成绩提取工具\n');
    console.log('=' .repeat(80) + '\n');

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
    console.log('📌 页面标题:', await page.title());
    console.log('\n' + '=' .repeat(80));
    console.log('📋 操作说明:');
    console.log('=' .repeat(80) + '\n');
    console.log('⏳ 浏览器将保持打开 120 秒 (2分钟)\n');
    console.log('请在浏览器中完成以下操作:');
    console.log('  1. 如果未登录,请输入用户名和密码');
    console.log('  2. 输入验证码');
    console.log('  3. 点击"用户登录"按钮');
    console.log('  4. 登录后,点击导航栏的"我的成绩"查看详细成绩\n');
    console.log('💡 提示: 如果已经登录,直接点击"我的成绩"菜单\n');
    console.log('=' .repeat(80) + '\n');

    // 等待用户登录和查看成绩
    await page.waitForTimeout(120000);

    console.log('\n⏳ 时间到!正在提取页面信息...\n');

    // 获取当前页面信息
    const currentUrl = page.url();
    const currentTitle = await page.title();

    console.log('📍 当前页面信息:');
    console.log('   URL:', currentUrl);
    console.log('   标题:', currentTitle);
    console.log('');

    // 截图当前页面
    await page.screenshot({
      path: 'gxpf-detailed-scores.png',
      fullPage: true
    });
    console.log('📸 当前页面截图已保存: gxpf-detailed-scores.png\n');

    // 保存页面HTML
    const htmlContent = await page.content();
    fs.writeFileSync('gxpf-detailed-scores.html', htmlContent, 'utf-8');
    console.log('💾 页面HTML已保存: gxpf-detailed-scores.html\n');

    // 提取页面文本
    console.log('📊 正在分析页面内容...\n');

    const pageText = await page.textContent('body');

    // 查找关键信息
    const info = {
      查询时间: new Date().toLocaleString('zh-CN'),
      当前URL: currentUrl,
      页面标题: currentTitle,
    };

    // 提取用户信息
    if (pageText.includes('在线用户数')) {
      const match = pageText.match(/在线用户数[：:]\s*(\d+)/);
      if (match) {
        info.在线用户数 = match[1];
      }
    }

    // 提取成绩相关信息
    const scoreKeywords = {
      '考试次数': /考试次数[：:\s]*(\d+)/,
      '合格次数': /合格次数[：:\s]*(\d+)/,
      '练习次数': /练习次数[：:\s]*(\d+)/,
      '学习次数': /学习次数[：:\s]*(\d+)/,
      '获得学时': /获得学时[：:\s]*(\d+)/,
    };

    console.log('📋 提取到的信息:\n');
    for (const [key, regex] of Object.entries(scoreKeywords)) {
      const match = pageText.match(regex);
      if (match) {
        info[key] = match[1];
        console.log(`  ✅ ${key}: ${match[1]}`);
      }
    }

    // 查找表格数据
    console.log('\n📊 正在查找表格和列表...\n');

    const tables = await page.locator('table, .el-table').all();
    console.log(`找到 ${tables.length} 个表格\n`);

    const scoreData = [];

    // 提取所有表格数据
    for (let i = 0; i < tables.length; i++) {
      try {
        const table = tables[i];
        const rows = await table.locator('tr, .el-table__row').all();

        if (rows.length > 0) {
          console.log(`=== 表格 ${i + 1} (${rows.length} 行) ===`);

          for (let j = 0; j < Math.min(rows.length, 50); j++) {
            const row = rows[j];
            const cells = await row.locator('td, th, .el-table__cell').all();
            const cellTexts = [];

            for (const cell of cells) {
              const text = await cell.textContent();
              if (text && text.trim()) {
                cellTexts.push(text.trim());
              }
            }

            if (cellTexts.length > 0) {
              const rowText = cellTexts.join(' | ');
              console.log(`  ${rowText}`);
              scoreData.push({
                表格: i + 1,
                行号: j + 1,
                数据: cellTexts
              });
            }
          }
          console.log('');
        }
      } catch (error) {
        console.log(`  ⚠️ 表格 ${i + 1} 解析失败:`, error.message);
      }
    }

    // 查找列表项
    console.log('📋 正在查找列表数据...\n');
    const listItems = await page.locator('li, .el-timeline-item').all();
    console.log(`找到 ${listItems.length} 个列表项\n`);

    for (let i = 0; i < Math.min(listItems.length, 20); i++) {
      try {
        const item = listItems[i];
        const text = await item.textContent();
        if (text && text.trim()) {
          console.log(`  ${i + 1}. ${text.trim()}`);
          scoreData.push({
            类型: '列表',
            序号: i + 1,
            内容: text.trim()
          });
        }
      } catch (error) {
        // 跳过失败的项
      }
    }

    // 保存提取的数据
    if (Object.keys(info).length > 0) {
      fs.writeFileSync(
        'exam-info.json',
        JSON.stringify(info, null, 2),
        'utf-8'
      );
      console.log('✅ 基本信息已保存: exam-info.json\n');
    }

    if (scoreData.length > 0) {
      fs.writeFileSync(
        'exam-score-details.json',
        JSON.stringify(scoreData, null, 2),
        'utf-8'
      );
      console.log('✅ 详细数据已保存: exam-score-details.json\n');

      // 生成 Markdown 报告
      let markdown = '# 广西普法考试成绩详细单\n\n';
      markdown += `**查询时间**: ${info.查询时间}\n`;
      if (info.在线用户数) markdown += `**在线用户数**: ${info.在线用户数}\n`;
      markdown += '\n---\n\n';

      // 基本信息
      markdown += '## 📊 基本信息\n\n';
      for (const [key, value] of Object.entries(info)) {
        if (key !== '查询时间' && key !== '在线用户数') {
          markdown += `- **${key}**: ${value}\n`;
        }
      }
      markdown += '\n';

      // 表格数据
      if (scoreData.length > 0) {
        markdown += '## 📋 详细数据\n\n';

        // 按表格分组
        const tableGroups = {};
        scoreData.forEach(item => {
          if (item.表格) {
            if (!tableGroups[item.表格]) {
              tableGroups[item.表格] = [];
            }
            tableGroups[item.表格].push(item);
          }
        });

        for (const [tableNum, items] of Object.entries(tableGroups)) {
          markdown += `### 表格 ${tableNum}\n\n`;
          items.forEach(item => {
            markdown += `${item.行号}. ${item.数据.join(' | ')}\n`;
          });
          markdown += '\n';
        }
      }

      fs.writeFileSync('exam-score-details.md', markdown, 'utf-8');
      console.log('📄 Markdown报告已保存: exam-score-details.md\n');
    }

    console.log('⏳ 浏览器将在 60 秒后关闭,你可以继续浏览...');
    await page.waitForTimeout(60000);

    console.log('\n✅ 任务完成!');
    console.log('\n📁 生成的文件:');
    console.log('   - gxpf-detailed-scores.png (页面截图)');
    console.log('   - gxpf-detailed-scores.html (页面HTML)');
    console.log('   - exam-info.json (基本信息)');
    console.log('   - exam-score-details.json (详细数据)');
    console.log('   - exam-score-details.md (成绩报告)');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('\n🔒 浏览器已关闭');
    }
  }
})();
