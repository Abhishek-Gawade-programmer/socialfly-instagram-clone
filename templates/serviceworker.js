var staticCacheName = 'djangopwa-v1';

self.addEventListener('install', function(event) {
event.waitUntil(
	console.log('sdgds')
	caches.open(staticCacheName).then(function(cache) {
	return cache.addAll([
		'',
	]);
	})
);
});

self.addEventListener('fetch', function(event) {
	console.log('sdgds')
var requestUrl = new URL(event.request.url);
	if (requestUrl.origin === location.origin) {
	if ((requestUrl.pathname === '/')) {
		event.respondWith(caches.match(''));
		return;
	}
	}
	event.respondWith(
	caches.match(event.request).then(function(response) {
		return response || fetch(event.request);
	})
	);
});
