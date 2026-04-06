import requests
from typing import Optional, Dict

def resolve_app_id(query: str) -> Optional[int]:
    """Resolves a user query to an App ID using Steam Store Search."""
    if query.isdigit():
        return int(query)
        
    url = f"http://store.steampowered.com/api/storesearch/?term={requests.utils.quote(query)}&l=english&cc=US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('items', [])
        if items:
            return items[0].get('id')
        return None
    except Exception as e:
        print(f"Error resolving name '{query}': {e}")
        return None

def fetch_reviews(app_id: int, count: int = 50) -> Dict[str, any]:
    """Fetches recent english reviews and separates them by sentiment."""
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1&language=english&filter=recent&num_per_page={count}"
    headers = {'User-Agent': 'SteamReviewSummarizer/1.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        reviews = data.get('reviews', [])
        pos_text = []
        neg_text = []
        
        for r in reviews:
            text = r.get('review', '').strip().replace('\n', ' ')
            if text:
                if r.get('voted_up', True):
                    pos_text.append(text)
                else:
                    neg_text.append(text)
                    
        return {
            "positive": "\n\n".join(pos_text),
            "negative": "\n\n".join(neg_text),
            "pos_count": len(pos_text),
            "neg_count": len(neg_text)
        }
        
    except Exception as e:
        print(f"Error fetching reviews for {app_id}: {e}")
        return {"positive": "", "negative": "", "pos_count": 0, "neg_count": 0}
