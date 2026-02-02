// Pricing Page Handler
function selectPlan(planId) {
    // Check if user is logged in
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!user.email) {
        // Not logged in, go to register with plan
        localStorage.setItem('selectedPlan', planId);
        window.location.href = `/register?plan=${planId}`;
    } else {
        // Logged in, go to payment
        localStorage.setItem('selectedPlan', planId);
        window.location.href = '/payment';
    }
}

// Load plans from API
document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/api/payment/plans');
        const data = await response.json();
        
        if (data.success) {
            console.log('Plans loaded:', data.plans);
            // Plans are already displayed in HTML, but we could dynamically update them here
        }
    } catch (error) {
        console.error('Error loading plans:', error);
    }
});
