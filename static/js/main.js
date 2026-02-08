// Main JavaScript for SignalTrust AI Market Scanner - Enhanced PWA
console.log('SignalTrust AI Market Scanner loaded');

// ====================================
// PWA INSTALLATION SUPPORT
// ====================================

let deferredPrompt;
const installBtn = document.createElement('button');
installBtn.className = 'pwa-install-btn';
installBtn.innerHTML = '📱 Install App';
installBtn.style.display = 'none';
document.body.appendChild(installBtn);

// Capture the beforeinstallprompt event
window.addEventListener('beforeinstallprompt', (e) => {
    console.log('[PWA] Install prompt available');
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;
    // Show install button
    installBtn.classList.add('show');
    installBtn.style.display = 'block';
});

// Handle install button click
installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) {
        console.log('[PWA] No install prompt available');
        return;
    }
    
    // Show the install prompt
    deferredPrompt.prompt();
    
    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`[PWA] User response to install prompt: ${outcome}`);
    
    if (outcome === 'accepted') {
        console.log('[PWA] User accepted the install prompt');
        installBtn.style.display = 'none';
    }
    
    // Clear the deferredPrompt
    deferredPrompt = null;
});

// Detect if app is installed
window.addEventListener('appinstalled', () => {
    console.log('[PWA] App installed successfully');
    installBtn.style.display = 'none';
    // Show welcome notification
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Welcome to SignalTrust AI!', {
            body: 'App installed successfully. You can now use it offline.',
            icon: '/static/icons/icon-192x192.png',
            badge: '/static/icons/icon-96x96.png'
        });
    }
});

// ====================================
// SERVICE WORKER REGISTRATION
// ====================================

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => {
                console.log('[SW] Registered successfully:', registration.scope);
                
                // Check for updates periodically
                setInterval(() => {
                    registration.update();
                }, 60000); // Check every minute
                
                // Handle service worker updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    console.log('[SW] New service worker installing...');
                    
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            console.log('[SW] New version available');
                            // Show update notification
                            showUpdateNotification();
                        }
                    });
                });
            })
            .catch(err => {
                console.error('[SW] Registration failed:', err);
            });
    });
}

// ====================================
// MOBILE OPTIMIZATIONS
// ====================================

// Prevent double-tap zoom and add visual feedback for touch events
let lastTouchEnd = 0;
document.addEventListener('touchstart', (e) => {
    if (e.target.matches('button, .btn, a.btn')) {
        e.target.style.transform = 'scale(0.97)';
    }
}, { passive: true });

document.addEventListener('touchend', (e) => {
    // Prevent double-tap zoom
    const now = Date.now();
    if (now - lastTouchEnd <= 300) {
        e.preventDefault();
    }
    lastTouchEnd = now;
    
    // Reset visual feedback for buttons
    if (e.target.matches('button, .btn, a.btn')) {
        setTimeout(() => {
            e.target.style.transform = '';
        }, 100);
    }
}, { passive: false }); // Can't be passive due to preventDefault

// Optimize scroll performance
let ticking = false;
let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
    lastScrollY = window.scrollY;
    if (!ticking) {
        window.requestAnimationFrame(() => {
            handleScroll(lastScrollY);
            ticking = false;
        });
        ticking = true;
    }
}, { passive: true });

function handleScroll(scrollY) {
    // Add scroll-based animations or effects here
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (scrollY > 50) {
            navbar.style.background = 'rgba(5, 8, 18, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.background = '';
            navbar.style.backdropFilter = '';
        }
    }
}

// ====================================
// NETWORK STATUS DETECTION
// ====================================

function updateOnlineStatus() {
    const status = navigator.onLine ? 'online' : 'offline';
    console.log(`[Network] Status: ${status}`);
    
    if (!navigator.onLine) {
        showOfflineNotification();
    } else {
        hideOfflineNotification();
    }
}

window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

// ====================================
// NOTIFICATION HELPERS
// ====================================

function showUpdateNotification() {
    const notification = document.createElement('div');
    notification.className = 'notification update-notification';
    notification.innerHTML = `
        <div style="padding: 16px; background: var(--bg-card); border-radius: 8px; box-shadow: var(--box-shadow-lg); display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.5rem;">🔄</span>
            <div style="flex: 1;">
                <strong>Update Available</strong>
                <p style="margin: 4px 0 0 0; font-size: 0.875rem; color: var(--text-secondary);">
                    A new version is available. Refresh to update.
                </p>
            </div>
            <button onclick="location.reload()" class="btn btn-primary" style="padding: 8px 16px;">
                Refresh
            </button>
        </div>
    `;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(notification);
}

function showOfflineNotification() {
    let notification = document.getElementById('offline-notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'offline-notification';
        notification.innerHTML = `
            <div style="padding: 12px 20px; background: #ff4444; color: white; text-align: center; font-weight: 600;">
                📡 You're offline. Some features may be limited.
            </div>
        `;
        notification.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 10000;
            animation: slideDown 0.3s ease;
        `;
        document.body.insertBefore(notification, document.body.firstChild);
    }
}

function hideOfflineNotification() {
    const notification = document.getElementById('offline-notification');
    if (notification) {
        notification.style.animation = 'slideUp 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }
}

// ====================================
// PERFORMANCE MONITORING
// ====================================

// Log performance metrics
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log('[Performance] Load time:', Math.round(perfData.loadEventEnd - perfData.fetchStart), 'ms');
                console.log('[Performance] DOM ready:', Math.round(perfData.domContentLoadedEventEnd - perfData.fetchStart), 'ms');
            }
        }, 0);
    });
}

// ====================================
// ANIMATIONS
// ====================================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideDown {
        from { transform: translateY(-100%); }
        to { transform: translateY(0); }
    }
    @keyframes slideUp {
        from { transform: translateY(0); }
        to { transform: translateY(-100%); }
    }
`;
document.head.appendChild(style);

// ====================================
// LAZY LOADING IMAGES
// ====================================

if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });
    
    // Observe all images with data-src attribute
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    });
}

// ====================================
// INITIALIZE
// ====================================

console.log('[PWA] SignalTrust AI initialized');
console.log('[PWA] App version: 2.0');
console.log('[PWA] Device:', /Mobile|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ? 'Mobile' : 'Desktop');
