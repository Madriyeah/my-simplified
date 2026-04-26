import requests
import re

# List of channels to scrape
channels = [
    {"name": "KSA Sports 1", "url": "https://aloula.sa"},
    {"name": "Rotana Khalejia", "url": "https://rotana.net"} 
]

def get_live_link(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        # Finds m3u8 links with tokens (Kwikmotion, Bozztv, etc.)
        match = re.search(r'https?://[^\s"\']+\.m3u8[^\s"\']*', response.text)
        return match.group(0) if match else None
    except:
        return None

# Start the M3U content
m3u_output = "#EXTM3U\n"

for ch in channels:
    print(f"Scraping {ch['name']}...")
    fresh_link = get_live_link(ch['url'])
    if fresh_link:
        m3u_output += f"#EXTINF:-1, {ch['name']}\n{fresh_link}\n"

# Save to your playlist file
with open("playlist.m3u", "w") as f:
    f.write(m3u_output)
