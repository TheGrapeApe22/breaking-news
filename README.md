# Discord preview links

Start the server with `npm start`, deploy it to a public HTTPS URL, then have the bot send a link in this form:

```
https://your-domain.example/preview?title=Hello%20there&body=A%20custom%20Discord%20preview&image=https%3A%2F%2Fexample.com%2Fimage.png
```

Encode every parameter before adding it to the URL. In JavaScript, build the link safely with:

```js
const url = new URL('/preview', 'https://your-domain.example');
url.search = new URLSearchParams({ title, body, image }).toString();
await channel.send(url.href);
```

Discord fetches the returned HTML itself and reads its Open Graph tags. It does not run browser JavaScript first, so a static page whose tags are altered from query parameters in client-side JavaScript will not create dynamic previews. This server renders the tags in its initial response instead.

`image` must be a publicly reachable absolute `http` or `https` URL. Discord may cache embeds; changing a link (for example, with a harmless `v` parameter) causes it to fetch a fresh preview.
