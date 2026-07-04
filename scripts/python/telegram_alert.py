#!/usr/bin/env python3
"""Мониторинг сервисов homelab с отправкой алертов в Telegram"""

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

SERVICES = {
    "Grafana": "http://192.168.1.152:3000",
    "Uptime Kuma": "http://192.168.1.152:3001",
    "SearXNG": "http://192.168.1.152:8090",
}

CHECK_INTERVAL = 30 


def send_alert(message: str) -> None:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})


def check_service(name: str, url: str) -> bool:
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


if __name__ == "__main__":
    while True:
        for name, url in SERVICES.items():
            if check_service(name, url):
                print(f"✅ {name} OK")
            else:
                print(f"❌ {name} недоступен")
                send_alert(f"⚠️ {name} упал!")
        time.sleep(CHECK_INTERVAL)
