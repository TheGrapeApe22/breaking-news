# Discord link preview server

Discord reads Open Graph tags from the initial HTML response. It does not wait for
browser JavaScript, so a static page cannot reliably set a different preview from
query parameters. This Flask app renders those tags on the server for each link.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

On Debian/Ubuntu, install `python3-venv` first if the first command reports that
`ensurepip` is unavailable: `sudo apt install python3-venv`.

Build links for the bot in this form (URL-encode each parameter):

```text
http://127.0.0.1:8000/?title=Hello&description=Optional%20body&image=https%3A%2F%2Fexample.com%2Fimage.png&site_name=My%20Site
```

`title` is required. `description` (or its supported alias, `body`), `image`, and
`site_name` are optional and produce empty Open Graph fields if omitted. `image`,
when supplied, must be an absolute HTTP or HTTPS URL that Discord can reach. The
returned page deliberately has an empty body, matching the supplied `index.html`;
its visible content is blank.

Discord caches previews aggressively. Use a newly generated link (for example,
add a harmless `v` parameter) when testing a changed preview.

## Deploy with Tailscale Funnel

The service must be public for Discord's crawler, so use **Funnel**, not
`tailscale serve` (which is tailnet-only).

1. Install and sign in to Tailscale on the machine that will run this app. Enable
   MagicDNS and approve Funnel if the CLI sends you to Tailscale's admin console.
2. Start the Python app and leave it running:

   ```bash
   source .venv/bin/activate
   python3 app.py
   ```

3. In a second terminal, publish it over HTTPS:

   ```bash
   tailscale funnel --bg 8000
   tailscale funnel status
   ```

   The status output gives a public `https://<machine>.<tailnet>.ts.net/` URL.
   Use that hostname in the bot's generated links, such as
   `https://<machine>.<tailnet>.ts.net/?title=Hello`.

Funnel needs HTTPS/MagicDNS and permission in your tailnet policy; it only exposes
HTTPS on Tailscale's supported public ports and applies its bandwidth limits. See
the official [Funnel documentation](https://tailscale.com/docs/reference/tailscale-cli/funnel).

To remove the public route later, run `tailscale funnel --https=443 off` (or use
the same port shown by `tailscale funnel status`).
