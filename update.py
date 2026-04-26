import requests
import re

# The official KSA Sports 1 live page
URL = "https://www.aloula.sa/en/live/ksa-sports1"

def get_ksa_link():
    try:
        # Use a real User-Agent to avoid being blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(URL, headers=headers, timeout=15)
        
        # Regex to find the kwikmotion .m3u8 link including the token
        match = re.search(r'https://live\.kwikmotion\.com/[^"\']+\.m3u8[^"\']*', response.text)
        
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Error: {e}")
    return None

new_link = get_ksa_link()

if new_link:
    # Create your Master M3U content
    m3u_content = f"#EXTM3U\n#EXTINF:-1, KSA Sports 1\n{new_link}\n"
    
    # Save it to a file
    with open("playlist.m3u", "w") as f:
        f.write(m3u_content)
    print("Playlist updated successfully.")
else:
    print("Could not find a new link.")
