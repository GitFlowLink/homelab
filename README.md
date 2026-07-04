# 🏠 Homelab Infrastructure

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Debian](https://img.shields.io/badge/Debian-A81D33?style=flat&logo=debian&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat&logo=ansible&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat&logo=terraform&logoColor=white)
![Yandex Cloud](https://img.shields.io/badge/Yandex%20Cloud-FF0000?style=flat&logo=yandexcloud&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![GitLab CI](https://img.shields.io/badge/GitLab%20CI-FC6D26?style=flat&logo=gitlab&logoColor=white)

Самохостируемая домашняя инфраструктура, управляемая как код — Docker-сервисы, Infrastructure as Code через Ansible + Terraform, стек мониторинга и провижининг в облаке Yandex Cloud.

---

## 🛠️ Скиллы, которые здесь применены

- **Configuration Management** — Ansible роли для настройки серверов, идемпотентные плейбуки, работа с inventory
- **Infrastructure as Code** — Terraform для провижининга VM в Yandex Cloud: переменные, outputs, паттерн `.tfvars`
- **Monitoring & Observability** — стек Prometheus + Grafana + Node Exporter с готовым дашбордом
- **CI/CD** — GitHub Actions (валидация YAML) и GitLab CI (build → test → deploy пайплайн)
- **Scripting** — Python (HTTP health-check, алерты в Telegram) и Bash автоматизация
- **Containerization** — Docker Compose для 8+ самохостящихся сервисов с грамотным управлением volumes
- **Networking** — кастомная маршрутизация трафика через прокси/VPN, настройка роутера на OpenWrt

---

## 🖥️ Железо

| Компонент | Характеристики |
|-----------|-----------------|
| Сервер | AMD A8, 8GB RAM, SSD 512GB |
| Роутер | Cudy WR3000S на OpenWrt |
| ОС | Debian Linux |

---

## 📦 Сервисы

### Медиа
- **[Jellyfin + Prowlarr](docker/mediaserver/)** — стриминг медиа и управление индексерами
- **[qBittorrent](docker/qbittorrent/)** — торрент-клиент с веб-интерфейсом

### Умный дом
- **[Home Assistant](docker/home-assistant/)** — локальная автоматизация умного дома без облака
- **[Mosquitto](docker/mosquitto/)** — MQTT брокер для IoT и ESP32 проектов

### Мониторинг и поиск
- **[Uptime Kuma](docker/uptime-kuma/)** — мониторинг доступности всех сервисов
- **[SearXNG](docker/searxng/)** — собственный поисковик без трекинга
- **[Prometheus + Grafana](docker/monitoring/)** — сбор метрик и визуализация ([подробнее ниже](#-мониторинг))

### Сеть
- **[Mihomo](network/mihomo/)** — прозрачный прокси на self-hosted VPS с VLESS+Reality, раздельная маршрутизация трафика

### Проекты
- **[DevOps Quiz](docker/devops-quiz-v2/)** — самохостируемый тренажёр DevOps знаний (Python + Nginx), со своим GitLab CI пайплайном

---

## ⚙️ Infrastructure as Code

### Ansible (`/ansible`)
Идемпотентные плейбуки для настройки серверов и деплоя сервисов.

- `playbook.yml` — базовая настройка сервера (пакеты, timezone, firewall) + деплой медиасервера
- `cloud-playbook.yml` — точка входа для облачных инстансов (используется Terraform)
- `update.yml` — обновление образов, перезапуск контейнеров, еженедельный cron
- `roles/base` — переиспользуемая роль для настройки ОС
- `roles/docker` — переиспользуемая роль для деплоя Docker Compose стеков

### Terraform + Yandex Cloud (`/terraform`)
Поднимает VM в Yandex Cloud и автоматически передаёт её Ansible для настройки — полный IaC-цикл от голого облака до работающих сервисов.

- `main.tf` — ресурс VM, cloud-init для SSH-доступа, `null_resource` провижионер который запускает Ansible сразу после старта VM
- `variables.tf` / `terraform.tfvars.example` — никакого хардкода секретов, все credentials передаются через `.tfvars`
- `outputs.tf` — выводит публичный/приватный IP VM после `apply`

```bash
cd terraform
terraform init
terraform apply   # поднимает VM + автоматически запускает Ansible
```

---

## 📊 Мониторинг

Стек Prometheus + Grafana + Node Exporter (`docker/monitoring/`), собирающий метрики уровня хоста (CPU, RAM, диск, сеть) с готовым дашбордом.

- `prometheus.yml` — конфиги scrape для self-monitoring и node-exporter
- `grafana.yml` — provisioning datasource (без ручной настройки через UI)

---

## 🔄 CI/CD

- **`.github/workflows/validate.yml`** — валидирует все YAML файлы (Ansible + Docker Compose) при каждом пуше через `yamllint`
- **`docker/devops-quiz-v2/.gitlab-ci.yml`** — пайплайн build → test → deploy для проекта DevOps Quiz

---

## 📜 Скрипты

### Python (`scripts/python/`)
- **`telegram_alert.py`** — HTTP health-check сервисов с уведомлениями в Telegram при падении, секреты через `.env`
- **`chiikawa_sync.py`** — автоматическая загрузка аниме серий (мониторинг Telegram-канала → библиотека Jellyfin), запускается через systemd таймер

### Bash (`scripts/bash/`)
- **`check_services.sh`** — проверка статуса Docker-контейнеров на удалённом хосте по SSH

---

## 📁 Структура репозитория

```
homelab/
├── ansible/          # Configuration management
├── terraform/        # Провижининг в облаке (Yandex Cloud)
├── docker/           # Все сервисы (Compose файлы)
├── scripts/          # Python + Bash автоматизация
├── network/          # Конфиги прокси/маршрутизации
└── .github/          # CI валидация
```

---
---

# 🏠 Homelab Infrastructure (EN)

Self-hosted home infrastructure managed as code — Docker services, Infrastructure as Code with Ansible + Terraform, a monitoring stack, and cloud provisioning in Yandex Cloud.

---

## 🛠️ Skills demonstrated

- **Configuration Management** — Ansible roles for server provisioning, idempotent playbooks, inventory management
- **Infrastructure as Code** — Terraform for Yandex Cloud VM provisioning: variables, outputs, `.tfvars` pattern
- **Monitoring & Observability** — Prometheus + Grafana + Node Exporter stack with a pre-built dashboard
- **CI/CD** — GitHub Actions (YAML validation) and GitLab CI (build → test → deploy pipeline)
- **Scripting** — Python (HTTP health checks, Telegram alerting) and Bash automation
- **Containerization** — Docker Compose for 8+ self-hosted services with proper volume management
- **Networking** — custom proxy/VPN traffic routing, OpenWrt router configuration

---

## 🖥️ Hardware

| Component | Specs |
|-----------|-------|
| Server | AMD A8, 8GB RAM, 512GB SSD |
| Router | Cudy WR3000S on OpenWrt |
| OS | Debian Linux |

---

## 📦 Services

### Media
- **[Jellyfin + Prowlarr](docker/mediaserver/)** — self-hosted media streaming and indexer management
- **[qBittorrent](docker/qbittorrent/)** — torrent client with web UI

### Smart Home
- **[Home Assistant](docker/home-assistant/)** — local home automation, no cloud
- **[Mosquitto](docker/mosquitto/)** — MQTT broker for IoT and ESP32 projects

### Monitoring & Search
- **[Uptime Kuma](docker/uptime-kuma/)** — uptime monitoring for all services
- **[SearXNG](docker/searxng/)** — self-hosted search engine, no tracking
- **[Prometheus + Grafana](docker/monitoring/)** — metrics collection and visualization ([see below](#-monitoring))

### Network
- **[Mihomo](network/mihomo/)** — transparent proxy on a self-hosted VPS with VLESS+Reality, split traffic routing

### Projects
- **[DevOps Quiz](docker/devops-quiz-v2/)** — self-hosted DevOps knowledge trainer (Python + Nginx), with its own GitLab CI pipeline

---

## ⚙️ Infrastructure as Code

### Ansible (`/ansible`)
Idempotent playbooks for server provisioning and service deployment.

- `playbook.yml` — base server setup (packages, timezone, firewall) + mediaserver deployment
- `cloud-playbook.yml` — provisioning entry point for cloud instances (used by Terraform)
- `update.yml` — pulls latest images, restarts containers, schedules weekly updates via cron
- `roles/base` — reusable role for OS-level configuration
- `roles/docker` — reusable role for deploying Docker Compose stacks

### Terraform + Yandex Cloud (`/terraform`)
Provisions a VM in Yandex Cloud and automatically hands it off to Ansible for configuration — a full IaC pipeline from bare cloud to running services.

- `main.tf` — VM resource, cloud-init for SSH access, `null_resource` provisioner that triggers Ansible right after the VM boots
- `variables.tf` / `terraform.tfvars.example` — no hardcoded secrets, credentials passed via `.tfvars`
- `outputs.tf` — exposes the VM's public/private IP after `apply`

```bash
cd terraform
terraform init
terraform apply   # provisions VM + runs Ansible automatically
```

---

## 📊 Monitoring

Prometheus + Grafana + Node Exporter stack (`docker/monitoring/`), scraping host-level metrics (CPU, RAM, disk, network) with a pre-built dashboard.

- `prometheus.yml` — scrape configs for self-monitoring and node-exporter
- `grafana.yml` — datasource provisioning (no manual UI setup needed)

---

## 🔄 CI/CD

- **`.github/workflows/validate.yml`** — validates all YAML files (Ansible + Docker Compose) on every push using `yamllint`
- **`docker/devops-quiz-v2/.gitlab-ci.yml`** — build → test → deploy pipeline for the DevOps Quiz project

---

## 📜 Scripts

### Python (`scripts/python/`)
- **`telegram_alert.py`** — HTTP health checks for services with Telegram notifications on downtime, secrets via `.env`
- **`chiikawa_sync.py`** — automated anime episode downloader (Telegram monitoring → Jellyfin library), runs via systemd timer

### Bash (`scripts/bash/`)
- **`check_services.sh`** — checks Docker container status on the remote host over SSH

---

## 📁 Repo structure

```
homelab/
├── ansible/          # Configuration management
├── terraform/        # Cloud provisioning (Yandex Cloud)
├── docker/           # All service stacks (Compose files)
├── scripts/          # Python + Bash automation
├── network/          # Proxy/routing configs
└── .github/          # CI validation workflow
```
