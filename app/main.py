from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from app.services.steam import resolve_app_id, fetch_reviews
from app.services.ai import summarize_text

app = FastAPI(title="Steam Game Review AI Summarizer")

# Request Model
class SummarizeRequest(BaseModel):
    query: str

class SummarizeResponse(BaseModel):
    app_id: int
    positive_summary: str
    negative_summary: str
    positive_percentage: float
    negative_percentage: float
    total_reviews_analyzed: int

@app.get("/api/summarize", response_model=SummarizeResponse)
async def get_summary(q: str = Query(..., description="Steam Game Name or App ID")):
    # 1. Resolve App ID
    app_id = resolve_app_id(q)
    if not app_id:
        raise HTTPException(status_code=404, detail="Game not found. Try entering an exact App ID.")
        
    # 2. Fetch Reviews separated by sentiment
    reviews_data = fetch_reviews(app_id, count=50)
    total_reviews = reviews_data["pos_count"] + reviews_data["neg_count"]
    
    if total_reviews == 0:
        raise HTTPException(status_code=404, detail="No reviews found for this game.")
        
    # 3. Calculate metrics
    pos_perc = (reviews_data["pos_count"] / total_reviews) * 100
    neg_perc = (reviews_data["neg_count"] / total_reviews) * 100
        
    # 4. Summarize Reviews separately
    pos_summary = summarize_text(reviews_data["positive"]) if reviews_data["positive"] else "No positive reviews to summarize."
    neg_summary = summarize_text(reviews_data["negative"]) if reviews_data["negative"] else "No negative reviews to summarize."
    
    return {
        "app_id": app_id,
        "positive_summary": pos_summary,
        "negative_summary": neg_summary,
        "positive_percentage": round(pos_perc, 1),
        "negative_percentage": round(neg_perc, 1),
        "total_reviews_analyzed": total_reviews
    }

# Mount static files at the root (must be after all endpoints)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
