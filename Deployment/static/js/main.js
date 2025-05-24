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
    
    // cluster descript based on cluster id 
    const clusterDescriptions = {
        0: "You belong to a segment of early solar adopters in rural areas with modest energy needs and cost savings. Your profile reflects a small household leveraging solar energy without subsidies. Consider applying for available government incentives to enhance your system’s return on investment.",
        1: "You are part of a high-consumption, biomass-reliant group with strong cost-saving performance but no financial assistance. This indicates a self-reliant approach in rural regions, though untapped support options may exist. Consider auditing your system and checking for regional programs that could further improve efficiency or reduce costs.",
        2: "You represent urban families benefiting from wind energy and government subsidies. Your adoption of clean energy is supported, and you're contributing to the shift in urban sustainability. Consider continuing engagement with policy updates and subsidy renewals to sustain this advantage.",
        3: "You are part of an early-adopter rural group with strong solar infrastructure and consistent long-term savings. This reflects resilience and long-term thinking in energy decisions. Maintain your system with regular evaluations to protect your early investment and ensure efficiency.",
        4: "You belong to a group with high energy usage and hydro adoption but limited financial return. Your profile suggests hydro may not be fully optimized or suited to your environment. Consider hybridizing with solar or evaluating household usage patterns to improve efficiency.",
        5: "You are part of a growing urban population independently using wind energy without subsidies. Despite the lack of financial support, your cost savings are commendable. Stay informed on evolving municipal energy policies — support may become available.",
        6: "You fall within a segment of urban families supported by subsidies while relying on hydro energy. Your energy usage is moderate, but performance could be further optimized. Consider installing smart systems or scheduling an energy audit to enhance cost-efficiency.",
        7: "You are part of an emerging rural group exploring geothermal solutions with partial support. Your profile reflects innovation in clean energy adoption. Ensure your system is properly maintained and aligned with geological suitability for geothermal.",
        8: "You represent a high-efficiency urban group achieving significant savings through wind energy without external support. Your household exemplifies effective clean energy management. Document and share your setup — your success could serve as a model for others.",
        9: "You belong to a strategic group of rural households achieving substantial cost savings through biomass without subsidy assistance. This demonstrates an effective and self-managed energy approach. Evaluate long-term biomass availability and environmental impact to sustain your trajectory."
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