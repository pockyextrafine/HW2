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
    summary: str
    original_reviews_count: int

@app.get("/api/summarize", response_model=SummarizeResponse)
async def get_summary(q: str = Query(..., description="Steam Game Name or App ID")):
    # 1. Resolve App ID
    app_id = resolve_app_id(q)
    if not app_id:
        raise HTTPException(status_code=404, detail="Game not found. Try entering an exact App ID.")
        
    # 2. Fetch Reviews
    reviews_text = fetch_reviews(app_id, count=50)
    if not reviews_text:
        raise HTTPException(status_code=404, detail="No reviews found for this game.")
        
    # 3. Summarize Reviews
    summary_result = summarize_text(reviews_text)
    
    return {
        "app_id": app_id,
        "summary": summary_result,
        "original_reviews_count": len(reviews_text.split('\n\n'))
    }

# Mount static files at the root (must be after all endpoints)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

