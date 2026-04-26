import requests
import re
import time

# Target page
SOURCE_URL = "https://www.elahmad.org/tv/live/channels.php?id=1092"
FILENAME = "playlist.m3u8"

def get_token_link():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.elahmad.org/'
    }
    
    session = requests.Session()
    try:
        # Step 1: Load main page
        print("Connecting to Elahmad...")
        r1 = session.get(SOURCE_URL, headers=headers, timeout=20)
        
        # Step 2: Find the iframe URL
        iframe_src = re.search(r'iframe.*?src=["\'](.*?)["\']', r1.text)
        if not iframe_src:
            print("Failed: No player frame found.")
            return None
            
        player_url = iframe_src.group(1)
        if player_url.startswith('//'): player_url = 'https:' + player_url
        
        # Step 3: Load the player page (where the token is generated)
        print(f"Fetching token from: {player_url}")
        r2 = session.get(player_url, headers=headers, timeout=20)
        
        # Step 4: Extract the .m3u8 link with wmsAuthSign
        # This looks for the link starting with https and ending with the full token
        link_match = re.search(r'(https://[^\s"\']+?\.m3u8\?wmsAuthSign=[^\s"\']+)', r2.text)
        
        if link_match:
            return link_match.group(1)
        
    except Exception as e:
        print(f"Error occurred: {e}")
    return None

def save_link(link):
    if link:
        with open(FILENAME, "w") as f:
            f.write(f"#EXTM3U\n#EXTINF:-1, Rotana Khalijia\n{link}")
        print("Success: playlist.m3u8 updated!")
    else:
        print("Error: Could not find a fresh link.")

if __name__ == "__main__":
    new_link = get_token_link()
    save_link(new_link)

