document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("search-form");
    const queryInput = document.getElementById("query-input");
    const submitBtn = document.getElementById("submit-btn");
    const btnText = submitBtn.querySelector(".btn-text");
    const btnLoader = document.getElementById("btn-loader");
    const errorMessage = document.getElementById("error-message");
    
    const resultsSection = document.getElementById("results");
    const reviewCount = document.getElementById("review-count");
    const summaryText = document.getElementById("summary-text");
    const steamLink = document.getElementById("steam-link");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        if (!query) return;

        // Reset state
        errorMessage.classList.add("hidden");
        resultsSection.classList.add("hidden");
        
        // Loading state
        submitBtn.disabled = true;
        btnText.classList.add("hidden");
        btnLoader.classList.remove("hidden");
        
        try {
            // Encode query safely
            const response = await fetch(`/api/summarize?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || "Failed to fetch summary.");
            }

            // Populate Results
            reviewCount.textContent = `Analyzed ${data.original_reviews_count} reviews`;
            summaryText.textContent = data.summary;
            steamLink.href = `https://store.steampowered.com/app/${data.app_id}`;
            
            // Show Results
            resultsSection.classList.remove("hidden");
            
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove("hidden");
        } finally {
            // Restore button state
            submitBtn.disabled = false;
            btnText.classList.remove("hidden");
            btnLoader.classList.add("hidden");
        }
    });
});
