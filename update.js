const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  let m3u8Link = "";

  // This part "listens" to the website's background traffic for the link
  page.on('request', request => {
    const url = request.url();
    if (url.includes('m3u8') && url.includes('wmsAuthSign')) {
      m3u8Link = url;
    }
  });

  try {
    console.log("Opening website...");
    await page.goto('https://elahmad.org', { waitUntil: 'networkidle2', timeout: 60000 });
    
    // Wait 25 seconds for the "20 second message" and player to load
    console.log("Waiting for player to generate token...");
    await new Promise(r => setTimeout(r, 25000));

    if (m3u8Link) {
      const content = `#EXTM3U\n#EXTINF:-1, Rotana Khalijia\n${m3u8Link}`;
      fs.writeFileSync('playlist.m3u8', content);
      console.log("Success! Link updated.");
    } else {
      console.log("Failed to find link. The site might be blocking the runner.");
    }
  } catch (err) {
    console.error("Error: ", err);
  } finally {
    await browser.close();
  }
})();

