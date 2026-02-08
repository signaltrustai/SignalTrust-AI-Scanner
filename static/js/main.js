// Main JavaScript for SignalTrust AI Market Scanner
console.log('SignalTrust AI Market Scanner loaded');

// =====================================================
// PWA Installation Support
// =====================================================

let deferredPrompt;
let installButton;

// Listen for beforeinstallprompt event
window.addEventListener('beforeinstallprompt', (e) => {
    console.log('beforeinstallprompt event fired');
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;
    // Show install button/banner if it exists
    showInstallPromotion();
});

// Function to show install promotion
function showInstallPromotion() {
    // Check if install button exists
    installButton = document.getElementById('pwa-install-btn');
    if (installButton) {
        installButton.style.display = 'block';
        installButton.addEventListener('click', installPWA);
    }
    
    // Show install banner if it exists
    const installBanner = document.getElementById('pwa-install-banner');
    if (installBanner) {
        installBanner.style.display = 'block';
        
        // Add close button handler
        const closeBtn = installBanner.querySelector('.close-banner');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                installBanner.style.display = 'none';
                // Remember user dismissed the banner
                localStorage.setItem('pwa-banner-dismissed', 'true');
            });
        }
        
        // Add install button handler in banner
        const bannerInstallBtn = installBanner.querySelector('.install-banner-btn');
        if (bannerInstallBtn) {
            bannerInstallBtn.addEventListener('click', installPWA);
        }
    }
}

// Function to trigger PWA installation
async function installPWA() {
    if (!deferredPrompt) {
        console.log('No deferred prompt available');
        return;
    }
    
    // Show the install prompt
    deferredPrompt.prompt();
    
    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`User response to the install prompt: ${outcome}`);
    
    // We've used the prompt, and can't use it again
    deferredPrompt = null;
    
    // Hide install UI
    if (installButton) {
        installButton.style.display = 'none';
    }
    const installBanner = document.getElementById('pwa-install-banner');
    if (installBanner) {
        installBanner.style.display = 'none';
    }
    
    // Show success message
    if (outcome === 'accepted') {
        console.log('User accepted the install prompt');
        showNotification('App installed successfully! 🎉', 'success');
    }
}

// Check if app is already installed
window.addEventListener('appinstalled', (e) => {
    console.log('PWA was installed successfully');
    showNotification('SignalTrust AI installed! Launch from your home screen.', 'success');
    // Hide install promotions
    if (installButton) {
        installButton.style.display = 'none';
    }
    const installBanner = document.getElementById('pwa-install-banner');
    if (installBanner) {
        installBanner.style.display = 'none';
    }
});

// Detect if running as PWA
function isRunningAsPWA() {
    return (window.matchMedia('(display-mode: standalone)').matches) || 
           (window.navigator.standalone) || 
           document.referrer.includes('android-app://');
}

// Show different UI if running as installed PWA
if (isRunningAsPWA()) {
    console.log('Running as installed PWA');
    document.body.classList.add('pwa-mode');
}

// =====================================================
// Service Worker Registration & Updates
// =====================================================

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then((registration) => {
                console.log('Service Worker registered:', registration);
                
                // Check for updates periodically (every 5 minutes to save battery)
                setInterval(() => {
                    registration.update();
                }, 300000); // Check every 5 minutes
                
                // Also check when page becomes visible (user returns to app)
                if ('visibilityState' in document) {
                    document.addEventListener('visibilitychange', () => {
                        if (!document.hidden) {
                            registration.update();
                        }
                    });
                }
                
                // Handle service worker updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            // New service worker available, show update prompt
                            showUpdatePrompt();
                        }
                    });
                });
            })
            .catch((err) => {
                console.log('Service Worker registration failed:', err);
            });
    });
}

// Show update prompt when new version is available
function showUpdatePrompt() {
    const updateBanner = document.createElement('div');
    updateBanner.className = 'update-banner';
    updateBanner.innerHTML = `
        <div class="update-content">
            <span>🔄 New version available!</span>
            <button class="btn btn-sm btn-primary" onclick="window.location.reload()">Update Now</button>
            <button class="btn btn-sm btn-outline" onclick="this.parentElement.parentElement.remove()">Later</button>
        </div>
    `;
    document.body.appendChild(updateBanner);
}

// =====================================================
// Offline Detection
// =====================================================

function updateOnlineStatus() {
    const isOnline = navigator.onLine;
    const statusIndicator = document.getElementById('online-status');
    
    if (statusIndicator) {
        if (isOnline) {
            statusIndicator.className = 'status-online';
            statusIndicator.textContent = '● Online';
        } else {
            statusIndicator.className = 'status-offline';
            statusIndicator.textContent = '● Offline';
        }
    }
    
    // Show notification on status change
    if (!isOnline) {
        showNotification('You are offline. Some features may be unavailable.', 'warning');
    } else {
        showNotification('Back online!', 'success');
    }
}

window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

// Initial status check
updateOnlineStatus();

// =====================================================
// Notification Helper
// =====================================================

function showNotification(message, type = 'info') {
    // Check if notification function exists (from other scripts)
    if (typeof window.showToast === 'function') {
        window.showToast(message, type);
        return;
    }
    
    // Fallback: simple console notification
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Create simple notification banner
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#00ff88' : type === 'warning' ? '#ffd700' : '#00d4ff'};
        color: #000;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// =====================================================
// Mobile-Specific Optimizations
// =====================================================

// Prevent pull-to-refresh on mobile if running as PWA
if (isRunningAsPWA()) {
    document.body.addEventListener('touchmove', (e) => {
        if (e.touches.length > 1) return; // Allow pinch zoom
        
        const target = e.target;
        const scrollable = target.closest('.scrollable');
        
        if (!scrollable) {
            e.preventDefault();
        }
    }, { passive: false });
}

// Add mobile touch optimizations
if ('ontouchstart' in window) {
    document.body.classList.add('touch-device');
}
