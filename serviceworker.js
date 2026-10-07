const CACHE_NAME = 'hangarin-pwa-v1';

const urlsToCache = [
    '/',
    '/offline/'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );

    self.skipWaiting();
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames
                    .filter(function(cacheName) {
                        return cacheName !== CACHE_NAME;
                    })
                    .map(function(cacheName) {
                        return caches.delete(cacheName);
                    })
            );
        })
    );

    self.clients.claim();
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request)
            .catch(function() {
                return caches.match(event.request);
            })
    );
});