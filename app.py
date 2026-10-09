"""A tiny server-side Open Graph preview page for Discord links."""

from urllib.parse import urlencode
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

RICKROLL = 'https://discord.com/vanityurl/dotcom/steakpants/flour/flower/index11.html'

def remove_none_values(d) -> dict:
    return {k: v for k, v in d.items() if v is not None}

@app.get("/oembed.json")
def oembed():
    args = {
        'author_name': request.args.get("author", None),
        'author_url': RICKROLL,
        'provider_name': request.args.get("provider", None),
        'provider_url': RICKROLL,
    }
    return jsonify(remove_none_values(args))


@app.get("/")
def preview():
    args = request.args
    
    oembed_params = ['author', 'provider']
    oembed_values = {param: args.get(param, "") for param in oembed_params}
    oembed_url = request.url_root.rstrip("/") + "/oembed.json?" + urlencode(oembed_values)

    non_oembed_values = {k: args.get(k, "") for k in args.keys() if k not in oembed_params}
    non_oembed_values = remove_none_values(non_oembed_values)

    all_values = {
        "page_url": request.url_root.rstrip("/") + request.path,
        "oembed_url": oembed_url,
        "appear_url": RICKROLL,
        **non_oembed_values # these override the default values
    }
    
    return render_template(
        "preview.html",
        **all_values
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8284, debug=False)
