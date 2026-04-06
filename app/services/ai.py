from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

_tokenizer = None
_model = None

def get_summarizer():
    global _tokenizer, _model
    if _model is None:
        print("Loading Lightweight AI Summarization Model...")
        model_name = "Falconsai/text_summarization"
        
        # Load raw model and tokenizer to bypass missing pipeline tasks in this transformers version
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        print("Model Loaded successfully!")
    return _tokenizer, _model

def summarize_text(text: str) -> str:
    """Takes review text and generates a concise summary using raw Seq2Seq module."""
    if not text.strip():
        return "No text provided to summarize."
        
    tokenizer, model = get_summarizer()
    
    # Truncate text string before tokenization to save time. 
    # 50 reviews can be long, so we'll take up to 8000 chars for processing.
    safe_text = text[:8000] 
    
    try:
        # T5 models expect a task prefix, Falconsai is often based on T5.
        input_text = "summarize: " + safe_text
        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate summary
        outputs = model.generate(**inputs, max_length=100, min_length=15, do_sample=False)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary
        
    except Exception as e:
        print(f"Summarizer error: {e}")
        return "Error: Could not summarize the reviews. Internal module error."
