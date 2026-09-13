const http = require('node:http');

const PORT = Number(process.env.PORT || 3000);
const MAX_TEXT_LENGTH = 300;

function text(value, fallback) {
  return (value || fallback).slice(0, MAX_TEXT_LENGTH);
}

function escapeHtml(value) {
  return value.replace(/[&<>'\"]/g, (character) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;'
  })[character]);
}

function imageUrl(value) {
  try {
    const url = new URL(value);
    return ['http:', 'https:'].includes(url.protocol) ? url.href : null;
  } catch {
    return null;
  }
}

function page({ title, description, image, canonicalUrl }) {
  const safeTitle = escapeHtml(title);
  const safeDescription = escapeHtml(description);
  const safeImage = escapeHtml(image);
  const safeCanonicalUrl = escapeHtml(canonicalUrl);

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta property="og:title" content="${safeTitle}">
  <meta property="og:description" content="${safeDescription}">
  <meta property="og:image" content="${safeImage}">
  <meta property="og:url" content="${safeCanonicalUrl}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${safeTitle}">
  <meta name="twitter:description" content="${safeDescription}">
  <meta name="twitter:image" content="${safeImage}">
  <title>${safeTitle}</title>
</head>
<body></body>
</html>`;
}

const server = http.createServer((request, response) => {
  const host = request.headers.host || `localhost:${PORT}`;
  const requestUrl = new URL(request.url, `http://${host}`);

  if (requestUrl.pathname !== '/preview') {
    response.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
    response.end('Use /preview?title=...&description=...&image=https%3A%2F%2F...');
    return;
  }

  const title = text(requestUrl.searchParams.get('title'), 'Insert title here');
  // `body` is the short name used by the bot command; `description` is also
  // accepted so the endpoint remains intuitive to use directly.
  const description = text(
    requestUrl.searchParams.get('body') || requestUrl.searchParams.get('description'),
    'Insert description here.'
  );
  const image = imageUrl(requestUrl.searchParams.get('image'));

  if (!image) {
    response.writeHead(400, { 'content-type': 'text/plain; charset=utf-8' });
    response.end('The image query parameter must be an absolute http(s) URL.');
    return;
  }

  const protocol = request.headers['x-forwarded-proto'] === 'https' ? 'https' : 'http';
  const canonicalUrl = `${protocol}://${host}${requestUrl.pathname}${requestUrl.search}`;
  response.writeHead(200, {
    'content-type': 'text/html; charset=utf-8',
    'cache-control': 'public, max-age=300'
  });
  response.end(page({ title, description, image, canonicalUrl }));
});

server.listen(PORT, '0.0.0.0', () => console.log(`Preview server listening on port ${PORT}`));
