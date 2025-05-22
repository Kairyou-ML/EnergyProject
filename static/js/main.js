document.addEventListener('DOMContentLoaded', function() {
    // Analysis form
    const analysisForm = document.getElementById('analysis-form');
    if (analysisForm) {
        analysisForm.addEventListener('submit', handleFormSubmit);
    }
});

/**
 * Handle form sub 
 * @param {Event} e 
 */
function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = this;
    const formData = new FormData(form);
    
    // boolen in check boxes
    if (!formData.has('urban')) formData.append('urban', 'false');
    if (!formData.has('subsidy')) formData.append('subsidy', 'false');
    
    // loading 
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
    submitButton.disabled = true;
    
    // Send data for analysis
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Restore button state
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
        
        if (data.success) {
            displayAnalysisResult(data.cluster_id, data.user_label);
        } else {
            displayError(data.error);
        }
    })
    .catch(error => {
        // Restore button state
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
        
        displayError('Server error: ' + error);
    });
}

/**
 *  result
 * @param {number} clusterId 
 * @param {string} userLabel - lab descrip
 */
function displayAnalysisResult(clusterId, userLabel) {
    document.getElementById('cluster-id').textContent = clusterId;
    document.getElementById('user-label').textContent = userLabel;
    
    // cluster descript based on cluster id ( ai generate)
    const clusterDescriptions = {
        0: "You belong to a group characterized by high energy usage in areas with limited energy infrastructure. Consider efficiency upgrades and exploring renewable alternatives.",
        1: "You're part of a rural household group that can benefit significantly from clean energy adoption. Solar and wind solutions work well for your profile.",
        2: "Your household uses minimal energy but has financial capacity for advanced solutions. Consider investing in cutting-edge energy technologies.",
        3: "As an urban resident receiving subsidies, you're already on the right track. Focus on maximizing the benefits of your current subsidized systems.",
        4: "You're budget-conscious in an urban setting. Look for cost-effective efficiency upgrades and community energy programs.",
        5: "You've achieved good energy efficiency in your urban home. Consider sharing your successful strategies with your community.",
        6: "Despite high energy consumption, your current setup isn't delivering optimal returns. Energy audits and targeted upgrades may help.",
        7: "You've achieved excellent cost savings despite modest means. Your approach could serve as a model for others in similar circumstances.",
        8: "Your urban household has higher-than-average energy expenditure. Consider smart home technologies to better manage consumption.",
        9: "As a higher-income household benefiting from subsidies, you might explore additional ways to maximize the environmental impact of your energy choices."
    };
    
    document.getElementById('cluster-description').textContent = clusterDescriptions[clusterId];
    
    document.getElementById('analysis-result-card').style.display = 'block';
    
    // Scroll 
    document.getElementById('analysis-result-card').scrollIntoView({ behavior: 'smooth' });
}

/**
 * eror handle
 * @param {string} errorMessage 
 */
function displayError(errorMessage) {
    alert('Error: ' + errorMessage);
} 