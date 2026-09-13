"""A tiny server-side Open Graph preview page for Discord links."""

from urllib.parse import urlparse

from flask import Flask, abort, render_template_string, request

app = Flask(__name__)


PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }}</title>
    <meta property="og:title" content="{{ title }}">
    <meta property="og:description" content="{{ description }}">
    <meta property="og:image" content="{{ image }}">
    <meta property="og:url" content="{{ page_url }}">
    <meta property="og:site_name" content="{{ site_name }}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{ title }}">
    <meta name="twitter:description" content="{{ description }}">
    <meta name="twitter:image" content="{{ image }}">
  </head>
  <body></body>
</html>
"""


def valid_image_url(value: str) -> bool:
    """Only pass ordinary public web URLs through to an Open Graph image tag."""
    if not value:
        return True
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


@app.get("/")
def preview():
    title = request.args.get("title", "").strip()
    # `body` is accepted for Discord bot code that uses that more natural name.
    description = request.args.get("description", request.args.get("body", ""))
    image = request.args.get("image", "").strip()
    site_name = request.args.get("site_name", "").strip()

    if not title:
        abort(400, "The title query parameter is required.")
    if not valid_image_url(image):
        abort(400, "image must be an absolute http(s) URL.")

    # Exclude the request's query string: it can contain arbitrary user input.
    page_url = request.url_root.rstrip("/") + request.path
    return render_template_string(
        PAGE,
        title=title,
        description=description,
        image=image,
        site_name=site_name,
        page_url=page_url,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
