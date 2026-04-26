const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--no-first-run',
      '--no-zygote',
      '--single-process',
      '--disable-gpu'
    ]
  });

  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
  await page.setExtraHTTPHeaders({ referer: 'https://elahmad.org/' });

  let m3u8Link = '';

  page.on('request', request => {
    const url = request.url();
    if (url.includes('.m3u8') && url.includes('wmsAuthSign')) {
      m3u8Link = url;
    }
  });

  try {
    await page.goto('https://elahmad.org', { waitUntil: 'networkidle2', timeout: 60000 });
    await page.goto('https://elahmad.org/tv/live/channels.php?id=1092', { waitUntil: 'networkidle2', timeout: 60000 });
    await page.waitForTimeout(30000);

    if (!m3u8Link) throw new Error('Could not capture m3u8 link');

    const content = `#EXTM3U\n#EXTINF:-1, Rotana Khalijia\n${m3u8Link}\n`;
    fs.writeFileSync('playlist.m3u8', content, 'utf8');
  } catch (err) {
    console.error(err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
