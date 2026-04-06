document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("search-form");
    const queryInput = document.getElementById("query-input");
    const submitBtn = document.getElementById("submit-btn");
    const btnText = submitBtn.querySelector(".btn-text");
    const btnLoader = document.getElementById("btn-loader");
    const errorMessage = document.getElementById("error-message");
    
    // Results DOM
    const resultsSection = document.getElementById("results");
    const reviewCount = document.getElementById("review-count");
    
    // Sentiment Bar
    const posLabel = document.getElementById("pos-label");
    const negLabel = document.getElementById("neg-label");
    const posBarFill = document.getElementById("pos-bar-fill");
    const negBarFill = document.getElementById("neg-bar-fill");
    
    // Summary Cards
    const posSummaryText = document.getElementById("pos-summary-text");
    const negSummaryText = document.getElementById("neg-summary-text");
    const steamLink = document.getElementById("steam-link");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        if (!query) return;

        errorMessage.classList.add("hidden");
        resultsSection.classList.add("hidden");
        
        submitBtn.disabled = true;
        btnText.classList.add("hidden");
        btnLoader.classList.remove("hidden");
        
        try {
            const response = await fetch(`/api/summarize?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || "Failed to fetch summary.");
            }

            // Populate Results
            reviewCount.textContent = `Analyzed ${data.total_reviews_analyzed} reviews`;
            
            // Populate Bars
            posLabel.textContent = `Positive ${data.positive_percentage}%`;
            negLabel.textContent = `Negative ${data.negative_percentage}%`;
            
            // Add a tiny buffer so bars aren't invisible if 0%
            posBarFill.style.width = Math.max(data.positive_percentage, 1) + "%";
            negBarFill.style.width = Math.max(data.negative_percentage, 1) + "%";

            // Summaries
            posSummaryText.textContent = data.positive_summary;
            negSummaryText.textContent = data.negative_summary;

            steamLink.href = `https://store.steampowered.com/app/${data.app_id}`;
            
            resultsSection.classList.remove("hidden");
            
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove("hidden");
        } finally {
            submitBtn.disabled = false;
            btnText.classList.remove("hidden");
            btnLoader.classList.add("hidden");
        }
    });
});
