import requests
import re

# The main page where the player is hosted
SOURCE_URL = "https://elahmad.org"
FILENAME = "playlist.m3u8"

def get_token_link():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://elahmad.org'
    }

    try:
        # 1. Get the main page content
        session = requests.Session()
        response = session.get(SOURCE_URL, headers=headers, timeout=15)
        
        # 2. Find the iframe source (where the actual player lives)
        iframe_match = re.search(r'iframe.*?src=["\'](.*?)["\']', response.text)
        if not iframe_match:
            print("Could not find the player iframe.")
            return None
        
        iframe_url = iframe_match.group(1)
        if iframe_url.startswith('//'):
            iframe_url = 'https:' + iframe_url

        # 3. Request the player page to find the .m3u8 link with the token
        player_resp = session.get(iframe_url, headers=headers, timeout=15)
        
        # This regex looks for the .m3u8 link containing wmsAuthSign
        token_link_match = re.search(r'(https://.*?\.m3u8\?.*?wmsAuthSign=[^"\'\s>]+)', player_resp.text)
        
        if token_link_match:
            return token_link_match.group(1)
        else:
            print("Token link not found in player page.")
            
    except Exception as e:
        print(f"Error: {e}")
    return None

def write_playlist(link):
    if link:
        content = f"#EXTM3U\n#EXTINF:-1, Rotana Khalijia\n{link}"
        with open(FILENAME, "w") as f:
            f.write(content)
        print(f"Updated {FILENAME} with new token.")
    else:
        print("Update failed: No link retrieved.")

if __name__ == "__main__":
    link = get_token_link()
    write_playlist(link)
