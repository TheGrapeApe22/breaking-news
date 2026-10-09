"""A tiny server-side Open Graph preview page for Discord links."""

from urllib.parse import urlencode, urlparse

from flask import Flask, abort, jsonify, render_template, request

app = Flask(__name__)


def valid_image_url(value: str) -> bool:
    """Only pass ordinary public web URLs through to an Open Graph image tag."""
    if not value:
        return True
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


@app.get("/oembed.json")
def oembed():
    """Return the oEmbed author and provider names supplied by the caller."""
    return jsonify(
        author_name=request.args.get("author_name", ""),
        author_url=request.args.get("author_url", ""),
        provider_name=request.args.get("provider_name", ""),
        provider_url=request.args.get("provider_url", ""),
    )


@app.get("/")
def preview():
    title = request.args.get("title", "").strip()
    # `body` is accepted for Discord bot code that uses that more natural name.
    description = request.args.get("description", request.args.get("body", ""))
    image = request.args.get("image", "").strip()
    site_name = request.args.get("site_name", "").strip()
    appear_url = request.args.get("appear_url", "").strip()
    large_image = request.args.get("large_image", "").strip().lower() != "false"
    oembed_params = {
        "author_name": request.args.get("author_name", ""),
        "provider_name": request.args.get("provider_name", ""),
        "author_url": request.args.get("author_url", ""),
        "provider_url": request.args.get("provider_url", ""),
    }

    if not valid_image_url(image):
        abort(400, "image must be an absolute http(s) URL.")

    # Exclude the request's query string: it can contain arbitrary user input.
    page_url = request.url_root.rstrip("/") + request.path
    oembed_url = request.url_root.rstrip("/") + "/oembed.json?" + urlencode(oembed_params)
    return render_template(
        "preview.html",
        title=title,
        description=description,
        image=image,
        site_name=site_name,
        page_url=page_url,
        oembed_url=oembed_url,
        large_image=bool(large_image),
        appear_url=appear_url if appear_url else 'https://discord.com/vanityurl/dotcom/steakpants/flour/flower/index11.html',
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8284, debug=False)
