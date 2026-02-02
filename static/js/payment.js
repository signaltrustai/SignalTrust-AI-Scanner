// Payment Form Handler
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('paymentForm');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    const cardNumber = document.getElementById('cardNumber');
    
    // Get user and plan info
    const pendingUser = JSON.parse(localStorage.getItem('pendingUser') || '{}');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const selectedPlan = localStorage.getItem('selectedPlan') || pendingUser.plan || 'pro';
    
    // Load plan details
    loadPlanDetails(selectedPlan);
    
    // Payment method switching
    const paymentTypeRadios = document.getElementsByName('paymentType');
    paymentTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            showPaymentFields(this.value);
        });
    });
    
    // Card number formatting and validation
    if (cardNumber) {
        cardNumber.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            e.target.value = formattedValue;
            
            // Validate in real-time
            if (value.length >= 13) {
                validateCardNumber(value);
            }
        });
    }
    
    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';
        
        const paymentType = document.querySelector('input[name="paymentType"]:checked').value;
        
        let paymentMethod = { type: paymentType };
        
        if (paymentType === 'card') {
            paymentMethod.card_number = document.getElementById('cardNumber').value.replace(/\s/g, '');
            paymentMethod.exp_month = document.getElementById('expMonth').value;
            paymentMethod.exp_year = document.getElementById('expYear').value;
            paymentMethod.cvv = document.getElementById('cvv').value;
            paymentMethod.cardholder_name = document.getElementById('cardName').value;
            
            // Validate card
            const validation = await validateCardNumber(paymentMethod.card_number);
            if (!validation.valid) {
                showError(validation.error || 'Invalid card number');
                return;
            }
            paymentMethod.last4 = validation.last4;
            
        } else if (paymentType === 'paypal') {
            paymentMethod.paypal_email = document.getElementById('paypalEmail').value;
        } else if (paymentType === 'crypto') {
            paymentMethod.wallet_address = document.getElementById('walletAddress').value;
        }
        
        const billingInfo = {
            email: document.getElementById('billingEmail').value,
            address: document.getElementById('billingAddress').value,
            city: document.getElementById('city').value,
            zip_code: document.getElementById('zipCode').value,
            country: document.getElementById('country').value
        };
        
        // Process payment
        try {
            const response = await fetch('/api/payment/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: pendingUser.user_id || user.user_id,
                    email: pendingUser.email || user.email,
                    plan_id: selectedPlan,
                    payment_method: paymentMethod,
                    billing_info: billingInfo
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showSuccess('Payment successful! Redirecting to dashboard...');
                
                // Clear pending user data
                localStorage.removeItem('pendingUser');
                localStorage.removeItem('selectedPlan');
                
                // Update user plan
                if (user.email) {
                    user.plan = selectedPlan;
                    user.payment_status = 'active';
                    localStorage.setItem('user', JSON.stringify(user));
                }
                
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                showError(data.error || 'Payment failed');
            }
        } catch (error) {
            showError('An error occurred processing your payment');
            console.error('Payment error:', error);
        }
    });
    
    async function validateCardNumber(cardNumber) {
        try {
            const response = await fetch('/api/payment/validate-card', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ card_number: cardNumber })
            });
            
            const data = await response.json();
            const validationDiv = document.getElementById('cardValidation');
            
            if (data.valid) {
                validationDiv.textContent = `✓ Valid ${data.card_type} card`;
                validationDiv.style.color = '#10b981';
            } else {
                validationDiv.textContent = `✗ ${data.error}`;
                validationDiv.style.color = '#ef4444';
            }
            
            return data;
        } catch (error) {
            console.error('Card validation error:', error);
            return { valid: false, error: 'Unable to validate card' };
        }
    }
    
    function showPaymentFields(type) {
        document.getElementById('cardFields').style.display = type === 'card' ? 'block' : 'none';
        document.getElementById('paypalFields').style.display = type === 'paypal' ? 'block' : 'none';
        document.getElementById('cryptoFields').style.display = type === 'crypto' ? 'block' : 'none';
    }
    
    async function loadPlanDetails(planId) {
        try {
            const response = await fetch('/api/payment/plans');
            const data = await response.json();
            
            if (data.success && data.plans[planId]) {
                const plan = data.plans[planId];
                
                document.getElementById('planName').textContent = plan.name;
                document.getElementById('planPrice').textContent = `$${plan.price.toFixed(2)}`;
                document.getElementById('subtotal').textContent = `$${plan.price.toFixed(2)}`;
                
                const tax = plan.price * 0.1;
                document.getElementById('tax').textContent = `$${tax.toFixed(2)}`;
                
                const total = plan.price + tax;
                document.getElementById('total').textContent = `$${total.toFixed(2)}`;
                
                // Update features list
                const featuresList = document.getElementById('featuresList');
                featuresList.innerHTML = '';
                plan.features.forEach(feature => {
                    const li = document.createElement('li');
                    li.textContent = `✓ ${feature}`;
                    featuresList.appendChild(li);
                });
            }
        } catch (error) {
            console.error('Error loading plan details:', error);
        }
    }
    
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        window.scrollTo(0, 0);
    }
    
    function showSuccess(message) {
        successMessage.textContent = message;
        successMessage.style.display = 'block';
        window.scrollTo(0, 0);
    }
});
