import httpx
import logging
import asyncio
import uvicorn
from pydantic import BaseSettings, SecretStr
from ipaddress import ip_address
from fastapi import FastAPI

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        style="{",
        fmt="[{name}:{filename}] {levelname} - {message}"
    )
)

log = logging.getLogger("tailscalesd")
log.setLevel(logging.DEBUG)
log.addHandler(handler)

DEVICES = []

def filter_ipv6(addresses):
    return list(filter(lambda a: ip_address(a).version == 4, addresses))

class Settings(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 9102
    interval: int = 5
    tailnet: str
    api_key: SecretStr

settings = Settings()
app = FastAPI()

async def tailscale_poll():
    global DEVICES
    log.debug("Starting polling")

    while True:
        async with httpx.AsyncClient() as client:
            # https://github.com/tailscale/tailscale/blob/main/api.md#tailnet-devices-get
            r = await client.get(
                f"https://api.tailscale.com/api/v2/tailnet/{settings.tailnet}/devices",
                auth=(settings.api_key.get_secret_value(), '')
            )
            DEVICES = r.json()['devices']

        await asyncio.sleep(settings.interval)

@app.on_event('startup')
async def start_tailscale_poll():
    asyncio.create_task(tailscale_poll())

@app.get('/')
async def sd():
    sd = []
    for device in DEVICES:
        # This was made mostly compatible with https://github.com/cfunkhouser/tailscalesd
        service = {}
        service['targets'] = filter_ipv6(device['addresses'])
        service['labels'] = {
            '__meta_tailscale_device_client_version': device['clientVersion'],
            '__meta_tailscale_device_hostname': device['hostname'],
            '__meta_tailscale_device_authorized': str(device['authorized']).lower(),
            '__meta_tailscale_device_id': device['id'],
            '__meta_tailscale_device_name': device['name'],
            '__meta_tailscale_device_os': device['os'],
            #'__meta_tailscale_device_tags': device.get('tags') or [],
            '__meta_tailscale_tailnet': settings.tailnet
        }

        sd.append(service)

    return sd

def main():
    #asyncio.run(tailscale_poll())
    uvicorn.run(app, host=settings.host, port=settings.port)

if __name__ == "__main__":
    main()
