# Homelab Infrastructure

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Debian](https://img.shields.io/badge/Debian-A81D33?style=flat&logo=debian&logoColor=white)
![OpenWrt](https://img.shields.io/badge/OpenWrt-00B5E2?style=flat&logo=openwrt&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat&logo=ansible&logoColor=white)

Self-hosted home server on a laptop — no cloud dependencies, full control over data and services.

---

## Hardware

| Component | Specs |
|-----------|-------|
| Server | AMD A8, 8GB RAM, SSD 512GB |
| Router | Cudy WR3000S on OpenWrt |
| OS | Debian Linux |

---

## Services

### Media
- **[Jellyfin](docker/jellyfin/)** — self-hosted media streaming instead of paid subscriptions
- **[qBittorrent](docker/qbittorrent/)** — torrent client with web UI
- **[Prowlarr](docker/prowlarr/)** — centralized indexer manager for the media stack

### Smart Home
- **[Home Assistant](docker/home-assistant/)** — local home automation, no cloud
- **[Mosquitto](docker/mosquitto/)** — MQTT broker for IoT devices and ESP32 projects

### Monitoring
- **[Uptime Kuma](docker/uptime-kuma/)** — uptime monitoring for all running services
- **[SearXNG](docker/searxng/)** — self-hosted search engine, no tracking

### Network
- **[Mihomo](network/mihomo/)** — traffic routing and filtering proxy

### Projects
- **[DevOps Quiz](docker/devops-quiz-v2/)** — self-hosted DevOps knowledge trainer (Python + Nginx)

---

## Automation

- All services run via Docker with `restart: unless-stopped`
- Systemd timers for scheduled tasks
- Ansible playbooks for server provisioning *(WIP)*

### Scripts

**[chiikawa_sync.py](scripts/chiikawa_sync.py)** — automated anime episode downloader
- Monitors a Telegram channel on schedule
- Downloads new episodes longer than 45 seconds
- Saves to Jellyfin library with correct naming convention
- Runs via systemd timer once a day
- Configured via environment variables

---

## Железо

| Компонент | Характеристики |
|-----------|----------------|
| Сервер | AMD A8, 8GB RAM, SSD 512GB |
| Роутер | Cudy WR3000S на OpenWrt |
| ОС | Debian Linux |

---

## Сервисы

### Медиа
- **[Jellyfin](docker/jellyfin/)** — стриминг медиа по локалке без платных подписок
- **[qBittorrent](docker/qbittorrent/)** — торрент клиент с веб-интерфейсом
- **[Prowlarr](docker/prowlarr/)** — централизованный менеджер индексеров для медиастека

### Умный дом
- **[Home Assistant](docker/home-assistant/)** — локальная автоматизация умного дома без облака
- **[Mosquitto](docker/mosquitto/)** — MQTT брокер для IoT и ESP32 проектов

### Мониторинг
- **[Uptime Kuma](docker/uptime-kuma/)** — мониторинг доступности всех сервисов
- **[SearXNG](docker/searxng/)** — собственный поисковик без трекинга

### Сеть
- **[Mihomo](network/mihomo/)** — маршрутизация и фильтрация трафика

### Проекты
- **[DevOps Quiz](docker/devops-quiz-v2/)** — самохостируемый тренажёр DevOps знаний (Python + Nginx)

---

## Автоматизация

- Все сервисы в Docker с `restart: unless-stopped`
- Systemd таймеры для плановых задач
- Ansible плейбуки для настройки сервера *(в разработке)*

### Скрипты

**[chiikawa_sync.py](scripts/chiikawa_sync.py)** — автоматическая загрузка аниме серий
- Проверяет Telegram канал по расписанию
- Скачивает новые серии длиннее 45 секунд
- Сохраняет в Jellyfin медиатеку с правильными именами
- Запускается через systemd таймер раз в сутки
- Конфигурация через переменные окружения
