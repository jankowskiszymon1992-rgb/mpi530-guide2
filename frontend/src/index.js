import React from "react";
import ReactDOM from "react-dom/client";
import "@/index.css";
import App from "@/App";

// Silently unregister all service workers and clear caches
try {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations()
      .then(function(regs) { regs.forEach(function(r) { r.unregister().catch(function(){}); }); })
      .catch(function(){});
  }
  if ('caches' in window) {
    caches.keys()
      .then(function(names) { names.forEach(function(n) { caches.delete(n).catch(function(){}); }); })
      .catch(function(){});
  }
} catch(e) {}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
