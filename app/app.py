from flask import Flask
import requests
import os

app = Flask(__name__)

# Credentials come from environment, not hardcoded
VAULT_ADDR  = os.environ["VAULT_ADDR"]
VAULT_TOKEN = os.environ["VAULT_TOKEN"]


def get_secret_from_vault():
    """Retrieves the api_key from Vault KV v2 at runtime."""
    try:
        resp = requests.get(
            f"{VAULT_ADDR}/v1/secret/data/app",
            headers={"X-Vault-Token": VAULT_TOKEN},
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()["data"]["data"]["api_key"], None
    except Exception as exc:
        return None, str(exc)


@app.route("/")
def index():
    secret, error = get_secret_from_vault()
    if error:
        return f"<h2>Vault Error</h2><pre>{error}</pre>", 500

    return f"""
    <!doctype html>
    <html>
    <head>
        <title>Exam App</title>
        <style>
            body {{ font-family: monospace; background: #1e1e2e; color: #cdd6f4;
                    display: flex; justify-content: center; padding-top: 80px; margin: 0; }}
            .card {{ background: #313244; border-radius: 12px; padding: 40px 60px;
                     box-shadow: 0 8px 32px rgba(0,0,0,0.4); max-width: 600px; width: 100%; }}
            h1 {{ color: #89b4fa; margin-bottom: 8px; }}
            .label {{ color: #a6adc8; font-size: 13px; margin-top: 24px; }}
            .secret {{ background: #1e1e2e; border: 1px solid #45475a; border-radius: 6px;
                       padding: 12px 16px; margin-top: 6px; color: #a6e3a1; word-break: break-all; }}
            .badge {{ display: inline-block; background: #a6e3a1; color: #1e1e2e;
                      border-radius: 4px; padding: 2px 8px; font-size: 12px; margin-left: 8px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Infrastructure Exam App <span class="badge">LIVE</span></h1>
            <p>All secrets are loaded at runtime from <strong>HashiCorp Vault</strong>.
               No credentials are present in source code or config files.</p>
            <div class="label">Secret retrieved from Vault → secret/app → api_key</div>
            <div class="secret">{secret}</div>
            <div class="label" style="margin-top:32px">Architecture</div>
            <div class="secret">Internet → Nginx :80 → Flask :5000 → Vault :8200</div>
        </div>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
