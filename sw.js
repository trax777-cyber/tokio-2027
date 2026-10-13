/* Service Worker: legt App, Schriften und Karten-Bibliothek ab, damit die App ohne Internet startet.
   Wird von quelle/build.py zu sw.js gebaut (Version und Dateiliste werden eingesetzt). */
const CACHE = "tokio-2027-61c3065536";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "vendor/fonts/fonts.css", "vendor/fonts/shippori-mincho-100-700-normal.woff2", "vendor/fonts/shippori-mincho-103-700-normal.woff2", "vendor/fonts/shippori-mincho-104-700-normal.woff2", "vendor/fonts/shippori-mincho-105-700-normal.woff2", "vendor/fonts/shippori-mincho-106-700-normal.woff2", "vendor/fonts/shippori-mincho-108-700-normal.woff2", "vendor/fonts/shippori-mincho-109-700-normal.woff2", "vendor/fonts/shippori-mincho-110-700-normal.woff2", "vendor/fonts/shippori-mincho-113-700-normal.woff2", "vendor/fonts/shippori-mincho-114-700-normal.woff2", "vendor/fonts/shippori-mincho-115-700-normal.woff2", "vendor/fonts/shippori-mincho-116-700-normal.woff2", "vendor/fonts/shippori-mincho-117-700-normal.woff2", "vendor/fonts/shippori-mincho-latin-700-normal.woff2", "vendor/fonts/source-sans-3-latin-400-normal.woff2", "vendor/fonts/source-sans-3-latin-500-normal.woff2", "vendor/fonts/source-sans-3-latin-600-normal.woff2", "vendor/fonts/source-sans-3-latin-ext-400-normal.woff2", "vendor/fonts/source-sans-3-latin-ext-500-normal.woff2", "vendor/fonts/source-sans-3-latin-ext-600-normal.woff2", "vendor/leaflet/images/layers-2x.png", "vendor/leaflet/images/layers.png", "vendor/leaflet/images/marker-icon-2x.png", "vendor/leaflet/images/marker-icon.png", "vendor/leaflet/images/marker-shadow.png", "vendor/leaflet/leaflet.css", "vendor/leaflet/leaflet.js"];
const INDEX = new URL("index.html", self.registration.scope).href;

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith("tokio-2027-") && k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;                 // Kartenkacheln, Google Maps usw. nicht anfassen
  if (req.mode === "navigate") {
    if (!(url.pathname.endsWith("/") || url.pathname.endsWith("/index.html"))) return;   // nur die App selbst
    e.respondWith(networkFirst(req));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req)));   // Schriften, Bibliothek, Symbole: aus dem Speicher
});

// Online: neueste Fassung holen und merken. Offline oder zu langsam (4 s): gemerkte Fassung.
function networkFirst(req) {
  const timeout = new Promise((_, reject) => setTimeout(reject, 4000));
  return Promise.race([fetch(req), timeout])
    .then(res => {
      if (res.ok) {
        const a = res.clone(), b = res.clone();
        caches.open(CACHE).then(c => { c.put(req, a); c.put(INDEX, b); });
      }
      return res;
    })
    .catch(() => caches.match(req, { ignoreSearch: true }).then(hit => hit || caches.match(INDEX)));
}
