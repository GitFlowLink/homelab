# Homelab Infrastructure

Домашний сервер на базе ноутбука — запускаю всё сам, не завишу от облаков.

## Железо
- **Основной сервер:** AMD A8, 8GB RAM, SSD 512GB
- **Второй нод:** планируется под AI/ML (Ollama, Whisper)
- **Роутер:** Cudy WR3000S на OpenWrt

## Сервисы

### Медиа
- **Jellyfin** — стримингoвый медиасервер
- **qBittorrent** — торрент клиент
- **Prowlarr** — менеджер индексеров

### Умный дом
- **Home Assistant** — автоматизация умного дома
- **Mosquitto** — MQTT брокер

### Мониторинг
- **Uptime Kuma** — мониторинг всех сервисов
- **SearXNG** — собственный поисковик

### Проекты
- **DevOps Quiz** — тренажёр DevOps знаний
- **FitTrack** — трекер тренировок

### Сеть
- **Mihomo** — маршрутизация и фильтрация трафика

## Автоматизация
- Docker с `restart: unless-stopped` на всех сервисах
- Systemd таймеры для плановых задач
- Ansible плейбуки для настройки сервера (в разработке)

---

# Homelab Infrastructure

Home server running on a laptop — self-hosted, no cloud dependencies.

## Hardware
- **Main server:** AMD A8, 8GB RAM, SSD 512GB
- **Second node:** planned for AI/ML workloads (Ollama, Whisper)
- **Router:** Cudy WR3000S on OpenWrt

## Services

### Media
- **Jellyfin** — streaming media server
- **qBittorrent** — torrent client
- **Prowlarr** — indexer manager

### Smart Home
- **Home Assistant** — home automation
- **Mosquitto** — MQTT broker

### Monitoring
- **Uptime Kuma** — uptime monitoring
- **SearXNG** — self-hosted search engine

### Projects
- **DevOps Quiz** — DevOps knowledge trainer
- **FitTrack** — personal fitness tracker

### Network
- **Mihomo** — traffic routing and filtering proxy

## Automation
- Docker with `restart: unless-stopped` on all services
- Systemd timers for scheduled tasks
- Ansible playbooks for server configuration (WIP)
