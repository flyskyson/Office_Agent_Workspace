const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;

  try {
    console.log('🚀 广西普法网 - 自动登录并提取成绩\n');
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
    console.log('\n开始自动登录...\n');

    // 等待页面加载
    await page.waitForTimeout(2000);

    // 查找并填写用户名
    console.log('📝 正在填写用户名...');
    const usernameInput = await page.locator('input[type="text"]').first();
    if (await usernameInput.isVisible()) {
      await usernameInput.fill('黎剑19731214');
      console.log('✅ 用户名已填写');
    }

    await page.waitForTimeout(500);

    // 查找并填写密码
    console.log('🔑 正在填写密码...');
    const passwordInput = await page.locator('input[type="password"]').first();
    if (await passwordInput.isVisible()) {
      await passwordInput.fill('Flyskylj@');
      console.log('✅ 密码已填写');
    }

    await page.waitForTimeout(500);

    // 截图登录前状态
    await page.screenshot({ path: 'gxpf-before-login.png' });
    console.log('📸 登录前截图已保存\n');

    console.log('⏳ 等待 30 秒供你输入验证码并点击登录...\n');
    console.log('💡 提示: 请手动输入验证码,然后点击"用户登录"按钮\n');
    console.log('=' .repeat(80) + '\n');

    // 等待用户手动输入验证码并登录
    await page.waitForTimeout(30000);

    console.log('⏳ 时间到!检查登录状态...\n');

    // 获取当前页面
    const currentUrl = page.url();
    console.log('📍 当前URL:', currentUrl);

    // 截图登录后状态
    await page.screenshot({
      path: 'gxpf-after-login.png',
      fullPage: true
    });
    console.log('📸 登录后截图已保存\n');

    // 点击"我的成绩"菜单
    console.log('🎯 正在点击"我的成绩"菜单...\n');

    try {
      // 查找"我的成绩"链接
      const scoreMenuLink = await page.locator('text=我的成绩').first();
      if (await scoreMenuLink.isVisible()) {
        await scoreMenuLink.click();
        console.log('✅ 已点击"我的成绩"菜单');

        // 等待页面加载
        await page.waitForTimeout(5000);

        // 截图成绩页面
        await page.screenshot({
          path: 'gxpf-scores-page.png',
          fullPage: true
        });
        console.log('📸 成绩页面截图已保存: gxpf-scores-page.png\n');
      }
    } catch (error) {
      console.log('⚠️ 未找到"我的成绩"菜单或点击失败');
    }

    // 保存当前页面HTML
    const htmlContent = await page.content();
    fs.writeFileSync('gxpf-final-page.html', htmlContent, 'utf-8');
    console.log('💾 页面HTML已保存: gxpf-final-page.html\n');

    // 提取页面文本
    console.log('📊 正在分析页面内容...\n');

    const pageText = await page.textContent('body');

    // 提取基本信息
    const info = {
      查询时间: new Date().toLocaleString('zh-CN'),
      用户名: '黎剑19731214',
      当前URL: page.url()
    };

    // 提取统计数据
    const stats = {
      '考试次数': /考试次数[：:\s]*(\d+)/.exec(pageText)?.[1],
      '合格次数': /合格次数[：:\s]*(\d+)/.exec(pageText)?.[1],
      '练习次数': /练习次数[：:\s]*(\d+)/.exec(pageText)?.[1],
      '学习次数': /学习次数[：:\s]*(\d+)/.exec(pageText)?.[1],
      '获得学时': /获得学时[：:\s]*(\d+)/.exec(pageText)?.[1]
    };

    console.log('📋 提取到的统计信息:\n');
    for (const [key, value] of Object.entries(stats)) {
      if (value) {
        console.log(`  ✅ ${key}: ${value}`);
        info[key] = value;
      }
    }

    // 查找并提取表格数据
    console.log('\n📊 正在查找成绩表格...\n');

    const scoreData = [];

    // 查找所有表格
    const tables = await page.locator('table, .el-table').all();
    console.log(`找到 ${tables.length} 个表格\n`);

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
        console.log(`  ⚠️ 表格 ${i + 1} 解析失败`);
      }
    }

    // 保存数据到文件
    if (Object.keys(info).length > 0) {
      const allInfo = { ...info, ...stats };
      fs.writeFileSync(
        'exam-final-info.json',
        JSON.stringify(allInfo, null, 2),
        'utf-8'
      );
      console.log('✅ 基本信息已保存: exam-final-info.json\n');
    }

    if (scoreData.length > 0) {
      fs.writeFileSync(
        'exam-final-scores.json',
        JSON.stringify(scoreData, null, 2),
        'utf-8'
      );
      console.log('✅ 详细成绩已保存: exam-final-scores.json\n');

      // 生成 Markdown 报告
      let markdown = '# 广西普法考试成绩单\n\n';
      markdown += `**查询时间**: ${info.查询时间}\n`;
      markdown += `**用户名**: ${info.用户名}\n\n`;
      markdown += '---\n\n';

      markdown += '## 📊 考试统计\n\n';
      markdown += '| 统计项 | 数据 |\n';
      markdown += '|--------|------|\n';
      for (const [key, value] of Object.entries(stats)) {
        if (value) {
          markdown += `| ${key} | ${value} |\n`;
        }
      }
      markdown += '\n';

      // 计算合格率
      if (stats['考试次数'] && stats['合格次数']) {
        const rate = (parseInt(stats['合格次数']) / parseInt(stats['考试次数']) * 100).toFixed(1);
        markdown += `### ✅ 合格率\n\n`;
        markdown += `- **合格次数/考试次数**: ${stats['合格次数']}/${stats['考试次数']}\n`;
        markdown += `- **合格率**: ${rate}%\n\n`;
      }

      markdown += '## 📋 详细成绩记录\n\n';

      // 按表格分组显示
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
        markdown += `### 成绩表格 ${tableNum}\n\n`;
        markdown += '| 序号';
        if (items[0] && items[0].数据) {
          for (let i = 0; i < items[0].数据.length; i++) {
            markdown += ` | 列${i + 1}`;
          }
        }
        markdown += ' |\n';
        markdown += '|------';
        for (let i = 0; i < (items[0]?.数据.length || 0); i++) {
          markdown += '|------';
        }
        markdown += '|\n';

        items.slice(0, 20).forEach(item => {
          markdown += `| ${item.行号}`;
          item.数据.forEach(cell => {
            markdown += ` | ${cell}`;
          });
          markdown += ' |\n';
        });
        markdown += '\n';
      }

      fs.writeFileSync('exam-final-report.md', markdown, 'utf-8');
      console.log('📄 Markdown报告已保存: exam-final-report.md\n');
    }

    // 保存Cookie供下次使用
    const cookies = await context.cookies();
    fs.writeFileSync('gxpf-cookies.json', JSON.stringify(cookies, null, 2), 'utf-8');
    console.log('🍪 Cookie已保存: gxpf-cookies.json');
    console.log('💡 下次可以使用Cookie直接登录,无需输入验证码\n');

    console.log('⏳ 浏览器将在 60 秒后关闭...');
    await page.waitForTimeout(60000);

    console.log('\n✅ 任务完成!');
    console.log('\n📁 生成的文件:');
    console.log('   - gxpf-before-login.png (登录前截图)');
    console.log('   - gxpf-after-login.png (登录后截图)');
    console.log('   - gxpf-scores-page.png (成绩页面截图)');
    console.log('   - gxpf-final-page.html (页面HTML)');
    console.log('   - exam-final-info.json (基本信息)');
    console.log('   - exam-final-scores.json (详细成绩)');
    console.log('   - exam-final-report.md (成绩报告)');
    console.log('   - gxpf-cookies.json (登录Cookie)');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
  } finally {
    if (browser) {
      await browser.close();
      console.log('\n🔒 浏览器已关闭');
    }
  }
})();
