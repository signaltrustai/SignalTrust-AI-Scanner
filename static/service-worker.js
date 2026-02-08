// SignalTrust AI — Service Worker v2.0 - Enhanced PWA Support
const CACHE_NAME = 'signaltrust-v3';
const RUNTIME_CACHE = 'signaltrust-runtime-v1';

// Core assets to cache on install
const CORE_ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png'
];

// Pages to cache for offline access
const OFFLINE_PAGES = [
  '/scanner',
  '/analyzer',
  '/predictions',
  '/ai-chat',
  '/pricing'
];

// Install — cache core assets
self.addEventListener('install', e => {
  console.log('[Service Worker] Installing...');
  e.waitUntil(
    Promise.all([
      // Cache core assets
      caches.open(CACHE_NAME).then(cache => {
        console.log('[Service Worker] Caching core assets');
        return Promise.allSettled(
          CORE_ASSETS.map(url => 
            cache.add(url).catch(err => {
              console.log(`[Service Worker] Failed to cache ${url}:`, err);
            })
          )
        );
      }),
      // Cache offline pages (try but don't fail install)
      caches.open(CACHE_NAME).then(cache => {
        console.log('[Service Worker] Caching offline pages');
        return Promise.allSettled(
          OFFLINE_PAGES.map(url => 
            cache.add(url).catch(err => {
              console.log(`[Service Worker] Failed to cache ${url}:`, err);
            })
          )
        );
      })
    ]).then(() => {
      console.log('[Service Worker] Install complete, skipping waiting');
      return self.skipWaiting();
    })
  );
});

// Activate — clean old caches and claim clients
self.addEventListener('activate', e => {
  console.log('[Service Worker] Activating...');
  e.waitUntil(
    caches.keys().then(keys => {
      const cacheWhitelist = [CACHE_NAME, RUNTIME_CACHE];
      return Promise.all(
        keys.map(key => {
          if (!cacheWhitelist.includes(key)) {
            console.log('[Service Worker] Deleting old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => {
      console.log('[Service Worker] Activation complete');
      return self.clients.claim();
    })
  );
});

// Fetch — network first with cache fallback for pages, cache first for assets
self.addEventListener('fetch', e => {
  const { request } = e;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip cross-origin requests
  if (url.origin !== self.location.origin) return;

  // Skip API requests (they need fresh data)
  if (url.pathname.startsWith('/api/')) return;

  // Strategy 1: Cache First for static assets (CSS, JS, images, icons)
  if (
    request.destination === 'style' ||
    request.destination === 'script' ||
    request.destination === 'image' ||
    url.pathname.includes('/static/')
  ) {
    e.respondWith(
      caches.match(request).then(cachedResponse => {
        if (cachedResponse) {
          console.log('[Service Worker] Cache hit (static):', url.pathname);
          return cachedResponse;
        }
        
        // Not in cache, fetch and cache
        return fetch(request).then(response => {
          // Check if valid response
          if (!response || response.status !== 200 || response.type === 'error') {
            return response;
          }
          
          // Clone the response
          const responseToCache = response.clone();
          
          caches.open(RUNTIME_CACHE).then(cache => {
            cache.put(request, responseToCache);
          });
          
          return response;
        });
      })
    );
    return;
  }

  // Strategy 2: Network First with Cache Fallback for HTML pages
  e.respondWith(
    fetch(request)
      .then(response => {
        // Check if valid response
        if (!response || response.status !== 200 || response.type === 'error') {
          return caches.match(request).then(cachedResponse => {
            return cachedResponse || response;
          });
        }
        
        // Clone and cache the response
        const responseToCache = response.clone();
        
        caches.open(CACHE_NAME).then(cache => {
          cache.put(request, responseToCache);
        });
        
        console.log('[Service Worker] Network response (page):', url.pathname);
        return response;
      })
      .catch(() => {
        // Network failed, try cache
        console.log('[Service Worker] Network failed, trying cache:', url.pathname);
        return caches.match(request).then(cachedResponse => {
          if (cachedResponse) {
            console.log('[Service Worker] Cache hit (offline):', url.pathname);
            return cachedResponse;
          }
          
          // If HTML page and not in cache, return offline page
          // Safely check accept header with null checks
          try {
            const acceptHeader = request.headers ? request.headers.get('accept') : null;
            if (acceptHeader && acceptHeader.includes('text/html')) {
              return caches.match('/').then(homeResponse => {
                return homeResponse || new Response(
                  '<h1>Offline</h1><p>You are offline and this page is not cached.</p>',
                  {
                    headers: { 'Content-Type': 'text/html' }
                  }
                );
              });
            }
          } catch (e) {
            console.log('[Service Worker] Error checking accept header:', e);
          }
          
          // For other resources, return error
          return new Response('Offline - Resource not cached', {
            status: 503,
            statusText: 'Service Unavailable'
          });
        });
      })
  );
});

// Background Sync for offline actions (future feature)
self.addEventListener('sync', event => {
  console.log('[Service Worker] Background sync:', event.tag);
  
  if (event.tag === 'sync-market-data') {
    event.waitUntil(syncMarketData());
  }
});

async function syncMarketData() {
  // Placeholder for syncing market data when back online
  console.log('[Service Worker] Syncing market data...');
  // Implementation would go here
}

// Push Notifications (future feature)
self.addEventListener('push', event => {
  console.log('[Service Worker] Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'New market update available!',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-96x96.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View Details',
        icon: '/static/icons/icon-96x96.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/icons/icon-96x96.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('SignalTrust AI', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  console.log('[Service Worker] Notification clicked:', event.action);
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Message handling from clients
self.addEventListener('message', event => {
  console.log('[Service Worker] Message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then(keys => {
        return Promise.all(keys.map(key => caches.delete(key)));
      })
    );
  }
});

console.log('[Service Worker] Loaded and ready');
