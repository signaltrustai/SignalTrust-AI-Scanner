// Root service worker proxy for SignalTrust AI
// Delegates to the main implementation in /static/service-worker.js
try {
  importScripts('/static/service-worker.js');
} catch (err) {
  console.error('Failed to import /static/service-worker.js; PWA functionality may be limited', err);
}
