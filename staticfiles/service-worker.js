const CACHE_NAME = 'church-attendance-v1';
const PRECACHE_URLS = [
  '/',
  '/events/',
  '/dashboard/',
  '/register/',
  '/offline.html',
];

// Install event: cache essential assets
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Precaching app shell');
      return cache.addAll(PRECACHE_URLS);
    })
  );
  self.skipWaiting();
});

// Activate event: clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[ServiceWorker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch event: serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Skip non-GET requests and external domains
  if (request.method !== 'GET' || !request.url.includes(self.location.origin)) {
    return;
  }

  // API requests: network first, fallback to cache
  if (request.url.includes('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache successful responses
          if (response.ok) {
            const cache = caches.open(CACHE_NAME);
            cache.then((c) => c.put(request, response.clone()));
          }
          return response;
        })
        .catch(() => {
          // Fallback to cache if offline
          return caches.match(request);
        })
    );
    return;
  }

  // Static assets & pages: cache first, fallback to network
  event.respondWith(
    caches.match(request).then((response) => {
      if (response) {
        return response;
      }
      return fetch(request)
        .then((networkResponse) => {
          // Cache successful responses
          if (networkResponse && networkResponse.status === 200) {
            const cache = caches.open(CACHE_NAME);
            cache.then((c) => c.put(request, networkResponse.clone()));
          }
          return networkResponse;
        })
        .catch(() => {
          // Offline fallback: return a minimal offline page if available
          if (request.mode === 'navigate') {
            return caches.match('/offline.html').catch(() => {
              return new Response(
                '<h1>You are offline</h1><p>Some features are unavailable. Please check your connection.</p>',
                { headers: { 'Content-Type': 'text/html' }, status: 503 }
              );
            });
          }
          return new Response('Offline', { status: 503 });
        });
    })
  );
});

// Push notifications
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  const options = {
    body: data.body || 'New notification from Church Attendance',
    icon: '/static/icons/icon-192.png',
    badge: '/static/icons/icon-96.png',
    tag: data.tag || 'church-notification',
    requireInteraction: data.requireInteraction || false,
  };
  event.waitUntil(
    self.registration.showNotification(data.title || 'Church Attendance', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const urlToOpen = event.notification.data?.url || '/';
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (let client of clientList) {
        if (client.url === urlToOpen && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(urlToOpen);
      }
    })
  );
});
