const { chromium } = require('playwright');
const fs = require('fs');

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

    console.log('🌐 正在访问淘宝...');

    // 访问淘宝首页
    await page.goto('https://www.taobao.com', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    console.log('📌 页面标题:', await page.title());

    // 等待搜索框加载
    await page.waitForTimeout(2000);

    // 找到搜索框并输入搜索内容
    console.log('\n🔍 正在搜索笔记本电脑...');
    const searchBox = await page.locator('#q').first();

    if (await searchBox.isVisible()) {
      await searchBox.fill('笔记本电脑 6000元');
      console.log('✅ 已输入搜索关键词');

      await page.waitForTimeout(1000);

      // 点击搜索按钮
      const searchButton = await page.locator('.btn-search').first();
      await searchButton.click();
      console.log('✅ 已点击搜索按钮');

      // 等待搜索结果加载
      await page.waitForTimeout(5000);

      // 截图保存搜索结果
      await page.screenshot({
        path: 'taobao-laptop-search.png',
        fullPage: true
      });
      console.log('📸 搜索结果截图已保存: taobao-laptop-search.png');

      // 尝试滚动页面加载更多内容
      console.log('\n📜 正在滚动加载更多商品...');
      for (let i = 0; i < 3; i++) {
        await page.evaluate(() => {
          window.scrollBy(0, window.innerHeight);
        });
        await page.waitForTimeout(2000);
      }

      // 提取商品信息
      console.log('\n📊 正在提取商品信息...');

      const products = await page.evaluate(() => {
        const items = [];
        const productCards = document.querySelectorAll('.Card--mainCard--3H6yQ');

        productCards.forEach((card, index) => {
          try {
            // 商品标题
            const titleElement = card.querySelector('.Card--title--2HAPN');
            const title = titleElement ? titleElement.textContent.trim() : '未知商品';

            // 价格
            const priceElement = card.querySelector('.Card--priceInt--3LrPc');
            const price = priceElement ? priceElement.textContent.trim() : '价格未知';

            // 销量
            const salesElement = card.querySelector('.Card--salesCount--1uJH5');
            const sales = salesElement ? salesElement.textContent.trim() : '未知';

            // 店铺名称
            const shopElement = card.querySelector('.Card--shopName--3kgJT');
            const shop = shopElement ? shopElement.textContent.trim() : '未知店铺';

            // 商品链接
            const linkElement = card.querySelector('a');
            const link = linkElement ? linkElement.href : '';

            items.push({
              序号: index + 1,
              商品名称: title.substring(0, 50), // 限制长度
              价格: price,
              销量: sales,
              店铺: shop,
              链接: link
            });
          } catch (error) {
            // 跳过解析失败的商品
          }
        });

        return items;
      });

      // 保存到 JSON 文件
      if (products.length > 0) {
        fs.writeFileSync(
          'laptop-list.json',
          JSON.stringify(products, null, 2),
          'utf-8'
        );
        console.log(`✅ 已提取 ${products.length} 个商品信息`);
        console.log('💾 数据已保存到: laptop-list.json');

        // 生成 Markdown 清单
        let markdown = '# 笔记本电脑清单 (6000元左右)\n\n';
        markdown += `**搜索时间**: ${new Date().toLocaleString('zh-CN')}\n`;
        markdown += `**商品数量**: ${products.length}\n\n`;
        markdown += '---\n\n';

        products.forEach(product => {
          markdown += `## ${product.序号}. ${product.商品名称}\n\n`;
          markdown += `- **价格**: ¥${product.价格}\n`;
          markdown += `- **销量**: ${product.销量}\n`;
          markdown += `- **店铺**: ${product.店铺}\n`;
          markdown += `- **链接**: [查看商品](${product.链接})\n\n`;
        });

        fs.writeFileSync('laptop-list.md', markdown, 'utf-8');
        console.log('📄 Markdown 清单已保存到: laptop-list.md');

        // 在控制台显示前 10 个商品
        console.log('\n' + '='.repeat(80));
        console.log('📋 商品清单预览 (前10个):');
        console.log('='.repeat(80) + '\n');

        products.slice(0, 10).forEach(product => {
          console.log(`${product.序号}. ${product.商品名称}`);
          console.log(`   价格: ¥${product.价格} | 销量: ${product.销量} | 店铺: ${product.店铺}`);
          console.log('');
        });

        console.log('='.repeat(80));
        console.log(`\n完整清单已保存到以下文件:`);
        console.log(`  - laptop-list.json (JSON格式)`);
        console.log(`  - laptop-list.md (Markdown格式)`);
        console.log(`  - taobao-laptop-search.png (搜索截图)`);
      } else {
        console.log('⚠️ 未能提取到商品信息');
      }
    } else {
      console.log('❌ 未找到搜索框');
    }

    // 保持浏览器打开 20 秒供查看
    console.log('\n⏳ 浏览器将在 20 秒后关闭...');
    await page.waitForTimeout(20000);

    console.log('\n✅ 任务完成!');

  } catch (error) {
    console.error('❌ 发生错误:', error.message);
    console.error(error.stack);
  } finally {
    if (browser) {
      await browser.close();
      console.log('\n🔒 浏览器已关闭');
    }
  }
})();
