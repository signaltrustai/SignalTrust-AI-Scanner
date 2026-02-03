// Registration Form Handler
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Clear previous messages
        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';
        
        // Get form values
        const fullName = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const plan = document.getElementById('plan').value;
        const agreeTerms = document.getElementById('agreeTerms').checked;
        
        // Validate
        if (password !== confirmPassword) {
            showError('Passwords do not match');
            return;
        }
        
        if (!agreeTerms) {
            showError('You must agree to the Terms of Service and Privacy Policy');
            return;
        }
        
        // Submit to API
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    full_name: fullName,
                    email: email,
                    password: password,
                    plan: plan
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showSuccess('Account created successfully! Redirecting...');
                
                // If plan is free, go to login
                if (plan === 'free') {
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 2000);
                } else {
                    // Go to payment page
                    setTimeout(() => {
                        localStorage.setItem('pendingUser', JSON.stringify({
                            user_id: data.user_id,
                            email: email,
                            plan: plan
                        }));
                        window.location.href = '/payment';
                    }, 2000);
                }
            } else {
                showError(data.error || 'Registration failed');
            }
        } catch (error) {
            showError('An error occurred. Please try again.');
            console.error('Registration error:', error);
        }
    });
    
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }
    
    function showSuccess(message) {
        successMessage.textContent = message;
        successMessage.style.display = 'block';
    }
});
