import requests
from datetime import datetime

# Sample backlinks to check
backlinks = [
    'https://example.com',
    'https://producthunt.com',
    'https://404-example.com',
    'https://otherlink.com',
]

# Dictionary to map URLs to target keywords
target_keywords = {
    'https://example.com': 'Keyword1',
    'https://producthunt.com': 'Keyword2',
    'https://otherlink.com': 'Keyword3',
}

# Store the status change times for removed links
link_removal_times = {}

# Function to check backlink status
def check_backlink_status(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        # Only return the status code if it's 404 or 200 (Present)
        if status_code == 404:
            return "404 - Not Found"
        elif status_code == 200:
            return "Present"
        else:
            return "Other"  # You can extend this to handle other status codes if needed
    except requests.exceptions.RequestException:
        return "Error"

# Function to get the target keyword for a URL
def get_target_keyword(url):
    return target_keywords.get(url, "Unknown Keyword")  # Default if not found

# Function to track when a link was removed
def track_removal_time(url, status):
    if status == "404 - Not Found" or status == "Error":
        if url not in link_removal_times:
            link_removal_times[url] = datetime.now()

# Loop through the backlinks and check the status
for url in backlinks:
    status = check_backlink_status(url)
    keyword = get_target_keyword(url)
    if status in ["404 - Not Found", "Present"]:
        print(f"URL: {url} | Status: {status} | Target Keyword: {keyword}")
        track_removal_time(url, status)

# Check and print the time of link removal if the link was removed
for url, removal_time in link_removal_times.items():
    print(f"Link {url} was removed on {removal_time}")
