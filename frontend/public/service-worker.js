/* Service worker disabled - cleanup only */
self.addEventListener('install', function() { self.skipWaiting(); });
self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(n) {
      return Promise.all(n.map(function(k) { return caches.delete(k); }));
    }).then(function() {
      return self.registration.unregister();
    }).catch(function(){})
  );
});
