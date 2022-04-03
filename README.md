# TailscaleSD - Prometheus Service Discovery for Tailscale (Python)

Serves Prometheus HTTP Service Discovery for devices on a Tailscale Tailnet.

This is a port of [@cfunkhouser's tailscalesd](https://github.com/cfunkhouser/tailscalesd) to Python.

This only uses the public API to enumerate devices.

# Usage

The `tailscalsd` server is configurable through environment variables.

### Mandatory:
- `TAILNET`: name of the tailnet to gather devices from. 
- `API_KEY`: Tailscale API token.

### Optional:
- `INTERVAL`: poll interval of the Tailscale API (default: every 5 seconds)
- `HOST`: host to serve TailscaleSD (default: `0.0.0.0`)
- `PORT`: port to server TailscaleSD (default: `9102`)

## Example

```
$~ TAILNET=bigchungus.com API_KEY=tskey-putyourapikeyhere tailscalesd
INFO:     Started server process [19650]
INFO:     Waiting for application startup.
[tailscalesd:__main__.py] DEBUG - Starting polling
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9102 (Press CTRL+C to quit)
```

# Prometheus Configuration

See [here](https://github.com/cfunkhouser/tailscalesd#prometheus-configuration) for an example of how to configure prometheus to scrape the data served by TailscaleSD.

# Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [byt3bl33d3r/pythoncookie](https://github.com/byt3bl33d3r/pythoncookie) project template.