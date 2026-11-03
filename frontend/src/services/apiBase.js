// Decides which address the browser should use for API requests.
// It is a plain function so it can be tested in Node without a browser.
export function chooseApiBase(hostname, port, protocol) {
  // In Codespaces, the FastAPI server also serves the UI on port 8000.
  // Same-origin requests avoid authentication/CORS issues between forwarded ports.
  if (/-8000\.app\.github\.dev$/.test(hostname)) {
    return "";
  }

  const codespaceMatch = hostname.match(/^(.*)-5173\.app\.github\.dev$/);

  if (codespaceMatch) {
    // Legacy compatibility for a Codespaces frontend opened on port 5173.
    return protocol + "//" + codespaceMatch[1] + "-8000.app.github.dev";
  }

  // Local development with the separate frontend server on port 5173.
  if (port === "5173") {
    return "http://127.0.0.1:8000";
  }

  // Everything else (Docker, Render, AWS, ...): FastAPI serves the page and the API
  // from the same address, so the browser uses the same origin.
  return "";
}
