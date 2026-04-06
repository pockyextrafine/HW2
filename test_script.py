import sys
import traceback
from app.services.steam import resolve_app_id, get_app_list, fetch_reviews
from app.services.ai import summarize_text

with open('debug_output.txt', 'w') as f:
    f.write("Testing Name Resolution for 'Portal 2'\n")
    app_id = resolve_app_id("Portal 2")
    f.write(f"Portal 2 App ID: {app_id}\n")

    f.write("Testing reviews fetch for 620\n")
    reviews = fetch_reviews(620)
    f.write(f"Reviews length: {len(reviews)}\n")

    f.write("Testing summarizer\n")
    try:
        summary = summarize_text(reviews)
        f.write(summary + "\n")
    except Exception as e:
        f.write(f"Error during summarization: {e}\n")
        f.write(traceback.format_exc())
