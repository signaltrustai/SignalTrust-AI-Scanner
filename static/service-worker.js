// SignalTrust AI — Service Worker v2.0 - Enhanced for Mobile PWA
const CACHE_VERSION = 'signaltrust-v3';
const CACHE_STATIC = `${CACHE_VERSION}-static`;
const CACHE_DYNAMIC = `${CACHE_VERSION}-dynamic`;
const CACHE_IMAGES = `${CACHE_VERSION}-images`;

// Core assets for offline functionality
const STATIC_ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/manifest.json'
];

// Install — cache core assets
self.addEventListener('install', event => {
  console.log('[ServiceWorker] Installing...');
  event.waitUntil(
    caches.open(CACHE_STATIC)
      .then(cache => {
        console.log('[ServiceWorker] Caching static assets');
        // Cache individually to avoid one failure blocking others
        return Promise.allSettled(
          STATIC_ASSETS.map(url => 
            cache.add(url).catch(err => {
              console.warn(`[ServiceWorker] Failed to cache: ${url}`, err);
            })
          )
        );
      })
      .then(() => self.skipWaiting())
  );
});

// Activate — clean old caches
self.addEventListener('activate', event => {
  console.log('[ServiceWorker] Activating...');
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(name => name.startsWith('signaltrust-') && !name.startsWith(CACHE_VERSION))
            .map(name => {
              console.log('[ServiceWorker] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => self.clients.claim())
  );
});

// Fetch — Optimized caching strategy for mobile
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests and external requests
  if (request.method !== 'GET' || url.origin !== location.origin) {
    return;
  }

  // API requests — Network only
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(fetch(request));
    return;
  }

  // Images — Cache first, network fallback
  if (request.destination === 'image' || url.pathname.match(/\.(jpg|jpeg|png|gif|svg|webp|ico)$/i)) {
    event.respondWith(
      caches.open(CACHE_IMAGES)
        .then(cache => {
          return cache.match(request)
            .then(cachedResponse => {
              if (cachedResponse) {
                return cachedResponse;
              }
              return fetch(request)
                .then(response => {
                  // Only cache successful responses
                  if (response.status === 200) {
                    cache.put(request, response.clone());
                  }
                  return response;
                })
                .catch(() => {
                  // Return placeholder image on error
                  return new Response(
                    '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" fill="#ccc"/></svg>',
                    { headers: { 'Content-Type': 'image/svg+xml' } }
                  );
                });
            });
        })
    );
    return;
  }

  // CSS/JS — Cache first, network fallback
  if (url.pathname.match(/\.(css|js)$/)) {
    event.respondWith(
      caches.match(request)
        .then(cachedResponse => {
          if (cachedResponse) {
            // Update cache in background
            fetch(request).then(response => {
              if (response.status === 200) {
                caches.open(CACHE_STATIC).then(cache => cache.put(request, response));
              }
            }).catch(() => {});
            return cachedResponse;
          }
          return fetch(request)
            .then(response => {
              if (response.status === 200) {
                caches.open(CACHE_STATIC).then(cache => cache.put(request, response.clone()));
              }
              return response;
            });
        })
    );
    return;
  }

  // HTML pages — Network first, cache fallback
  event.respondWith(
    fetch(request)
      .then(response => {
        // Cache successful responses
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_DYNAMIC)
            .then(cache => cache.put(request, responseClone))
            .catch(() => {});
        }
        return response;
      })
      .catch(() => {
        // Try cache
        return caches.match(request)
          .then(cachedResponse => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // Offline fallback page
            if (request.mode === 'navigate') {
              return caches.match('/');
            }
            return new Response('Offline', { status: 503 });
          });
      })
  );
});

// Background sync for offline actions (if supported)
self.addEventListener('sync', event => {
  console.log('[ServiceWorker] Background sync:', event.tag);
  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

// Push notifications (if supported)
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'New notification from SignalTrust AI',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-96x96.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    }
  };
  event.waitUntil(
    self.registration.showNotification('SignalTrust AI', options)
  );
});

// Helper function for syncing data
async function syncData() {
  try {
    // Sync any pending offline actions
    console.log('[ServiceWorker] Syncing offline data...');
    return true;
  } catch (error) {
    console.error('[ServiceWorker] Sync failed:', error);
    throw error;
  }
}
