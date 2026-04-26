const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  // These args are crucial for running on GitHub Actions
  const browser = await puppeteer.launch({ 
    headless: "new",
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
  // Set a real-looking user agent so the site doesn't block the browser
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

  let m3u8Link = "";

  page.on('request', request => {
    const url = request.url();
    if (url.includes('m3u8') && url.includes('wmsAuthSign')) {
      m3u8Link = url;
    }
  });

  try {
    console.log("Opening website...");
    // elahmad often checks for referers, so we go to the base site first
    await page.goto('https://elahmad.org', { waitUntil: 'networkidle2' });
    await page.goto('https://elahmad.org/tv/live/channels.php?id=1092', { waitUntil: 'networkidle2', timeout: 60000 });
    
    console.log("Waiting 30 seconds for player to load...");
    await new Promise(r => setTimeout(r, 30000));

    if (m3u8Link) {
      const content = `#EXTM3U\n#EXTINF:-1, Rotana Khalijia\n${m3u8Link}`;
      fs.writeFileSync('playlist.m3u8', content);
      console.log("SUCCESS: Link found and saved.");
    } else {
      console.log("ERROR: Could not capture the m3u8 link. The player might not have started.");
      process.exit(1); // Tell GitHub it failed so you can see the log
    }
  } catch (err) {
    console.error("CRASH: ", err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
