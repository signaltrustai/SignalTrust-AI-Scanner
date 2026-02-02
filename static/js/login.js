// Login Form Handler
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Clear previous messages
        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';
        
        // Get form values
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const rememberMe = document.getElementById('rememberMe').checked;
        
        // Submit to API
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showSuccess('Login successful! Redirecting...');
                
                // Store session token
                if (rememberMe) {
                    localStorage.setItem('sessionToken', data.session_token);
                } else {
                    sessionStorage.setItem('sessionToken', data.session_token);
                }
                
                // Store user data
                localStorage.setItem('user', JSON.stringify(data.user));
                
                // Check if payment is pending
                if (data.user.payment_status === 'pending') {
                    setTimeout(() => {
                        window.location.href = '/payment';
                    }, 1500);
                } else {
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1500);
                }
            } else {
                showError(data.error || 'Login failed');
            }
        } catch (error) {
            showError('An error occurred. Please try again.');
            console.error('Login error:', error);
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
