import requests
from typing import Optional

def resolve_app_id(query: str) -> Optional[int]:
    """Resolves a user query to an App ID using Steam Store Search."""
    # If the user passed directly an integer App ID
    if query.isdigit():
        return int(query)
        
    # Otherwise search by name using the much faster storesearch API
    url = f"http://store.steampowered.com/api/storesearch/?term={requests.utils.quote(query)}&l=english&cc=US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('items', [])
        if items:
            # First item is usually the most relevant game
            return items[0].get('id')
            
        return None
    except Exception as e:
        print(f"Error resolving name '{query}': {e}")
        return None

def fetch_reviews(app_id: int, count: int = 15) -> str:
    """Fetches recent english reviews for the given app_id."""
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1&language=english&filter=recent&num_per_page={count}"
    
    headers = {
        'User-Agent': 'SteamReviewSummarizer/1.0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        reviews = data.get('reviews', [])
        if not reviews:
            return ""
            
        # Extract text and concatenate
        extracted_text = []
        for r in reviews:
            # Clean up newlines or excessive whitespace
            text = r.get('review', '').strip().replace('\n', ' ')
            if text:
                extracted_text.append(text)
                
        # Join with a separator
        return "\n\n".join(extracted_text)
        
    except Exception as e:
        print(f"Error fetching reviews for {app_id}: {e}")
        return ""
