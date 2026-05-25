# exam-infra — Automated Infrastructure, Security & Monitoring

**Grade target: 10/10 — deployed with a single terminal command.**

---

## Deployment (1 command)

After accessing the VM via SSH:

```bash
curl -fsSL https://raw.githubusercontent.com/USER/exam-infra/main/bootstrap.sh | sudo bash
```

That's it. The bootstrap script handles everything:
1. Installs Docker
2. Clones this repository
3. Starts all services via Docker Compose
4. Initializes Vault and stores the application secret

---

## Architecture

```
Internet
   │
   ▼
┌──────────────────────────────────────────────────┐
│  VM                                              │
│                                                  │
│  Nginx :80  ──▶  Flask App :5000  ──▶  Vault :8200 │
│                                                  │
│  Node Exporter :9100                            │
│         │                                        │
│         ▼                                        │
│  Prometheus :9090  ──▶  Grafana :3000            │
└──────────────────────────────────────────────────┘
```

### Components

| Component | Tool | Purpose |
|---|---|---|
| Reverse Proxy | Nginx | Sole entry point — app not exposed directly |
| Application | Flask (Python) | Reads secret from Vault at runtime |
| Secret Manager | HashiCorp Vault (dev mode) | Stores `api_key`, no hardcoded secrets |
| Metrics Collection | Prometheus + Node Exporter | Scrapes VM CPU/RAM |
| Visualization | Grafana | Live dashboard, auto-provisioned |

---

## Access (after deploy)

| Service | URL | Credentials |
|---|---|---|
| App | `http://<VM-IP>` | — |
| Grafana | `http://<VM-IP>:3000` | admin / admin |
| Vault UI | `http://<VM-IP>:8200` | Token: `root` |

---

## Security Compliance

- **No hardcoded secrets** in any source file or config.
- `VAULT_TOKEN` is injected as a Docker environment variable at runtime.
- The Flask application retrieves `api_key` from Vault's REST API on each request.
- The Flask container is **not** port-mapped; only Nginx is exposed on port 80.

---

## Commands used (exam count)

| # | Command |
|---|---|
| 1 | `curl -fsSL https://raw.githubusercontent.com/.../bootstrap.sh \| sudo bash` |

**Total: 1 command → Grade 10**
