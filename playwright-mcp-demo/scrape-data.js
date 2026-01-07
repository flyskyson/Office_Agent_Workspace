const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    console.log('🌐 正在访问网页...');
    await page.goto('https://www.bilibili.com');

    // 等待页面加载
    await page.waitForLoadState('networkidle');

    // 提取页面标题
    const title = await page.title();
    console.log('📌 页面标题:', title);

    // 提取视频链接
    console.log('\n📺 正在提取视频链接...');
    const videoLinks = await page.$$eval('.video-card a', links =>
      links.slice(0, 5).map(link => ({
        title: link.textContent?.trim() || '无标题',
        url: link.href
      }))
    );

    console.log(`\n找到 ${videoLinks.length} 个视频:\n`);
    videoLinks.forEach((video, index) => {
      console.log(`${index + 1}. ${video.title}`);
      console.log(`   ${video.url}\n`);
    });

    // 保存到文件
    const fs = require('fs');
    fs.writeFileSync(
      'bilibili-videos.json',
      JSON.stringify(videoLinks, null, 2),
      'utf-8'
    );
    console.log('✅ 数据已保存到: bilibili-videos.json');

    await page.waitForTimeout(5000);
  } catch (error) {
    console.error('❌ 错误:', error.message);
  } finally {
    await browser.close();
  }
})();
