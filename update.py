import requests
import re

# Your target URL structure
BASE_URL = "https://tgn.bozztv.com/gin-36bay3/ga-rotanakhalija-gulf/tracks-v1a1/mono.ts.m3u8"

def get_latest_token():
    # Example: If the token is found on a webpage, scrape it here.
    # Replace this with the logic that finds the current working link.
    # For now, this is a placeholder for your specific fetching logic.
    source_url = "https://example.com" 
    response = requests.get(source_url)
    # Use regex to find the wmsAuthSign and session ID
    # token = re.search(r'wmsAuthSign=([^&" \n]+)', response.text).group(1)
    return "YOUR_FETCHED_TOKEN"

def update_playlist():
    # token = get_latest_token()
    # Replace with your actual logic to build the full link
    new_link = f"{BASE_URL}?nimblesessionid=...&wmsAuthSign=..."
    
    # Save the link to a file that your IPTV player can point to
    with open("playlist.m3u8", "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, Rotana Khalijia\n")
        f.write(new_link)

if __name__ == "__main__":
    update_playlist()
