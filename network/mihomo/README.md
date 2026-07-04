# Mihomo (Clash Meta)

Прозрачный прокси для гибкой маршрутизации трафика на базе [Mihomo](https://github.com/MetaCubeX/mihomo) — форк Clash Meta, работающий с self-hosted VPS.

## Архитектура

```
Устройства в сети
      ↓
Роутер OpenWrt (Cudy WR3000S)
      ↓
Mihomo (прозрачный прокси)
      ↓
Маршрутизация по правилам
   ↙        ↘
Прямое     Через прокси
соединение  (self-hosted VPS)
```

## Бэкенд

- **VPS** — self-hosted, Нидерланды, на нём поднят Xray
- **Протокол** — VLESS + Reality (основной), Hysteria2 (UDP резерв, высокая скорость)
- **Watchdog** — `mihomo-watchdog.sh` следит за процессом и перезапускает при падении (через systemd)

## Функции

- Прозрачный прокси — все устройства в сети работают автоматически, без настройки на каждом
- Раздельная маршрутизация — локальные/региональные ресурсы идут напрямую, остальное через прокси
- DNS over HTTPS — защита DNS запросов от перехвата и подмены
- Поддержка IPv4 и IPv6
- Автоматический fallback на прямое соединение при недоступности прокси

## Конфигурация

| Параметр | Значение |
|----------|----------|
| Сервис | systemd |
| Конфиг | `/etc/mihomo/config.yaml` |
| Веб-панель | `http://localhost:9090` |
| Автозапуск | `systemctl enable mihomo` |

> Конфигурационный файл не включён в репозиторий — содержит приватные данные (IP адрес сервера, ключи авторизации).

## Дебаг-кейсы

Реальные проблемы, с которыми пришлось разбираться в процессе эксплуатации:
- Отказ DNS-резолвинга при определённых правилах маршрутизации — причина оказалась в конфликте приоритета DNS-over-HTTPS и локального резолвера
- Противодействие блокировкам по SNI — смена fronting-доменов и подстройка TLS fingerprinting
- Переключение между режимами прозрачного прокси и rule-based без обрыва активных соединений

---
---

# Mihomo (Clash Meta) — EN

Transparent proxy for flexible traffic routing based on [Mihomo](https://github.com/MetaCubeX/mihomo) (Clash Meta fork), running on a self-hosted VPS.

## Architecture

```
Devices on LAN
      ↓
OpenWrt Router (Cudy WR3000S)
      ↓
Mihomo (transparent proxy)
      ↓
Rule-based routing
   ↙        ↘
Direct     Proxy (self-hosted VPS)
```

## Backend

- **VPS** — self-hosted, Netherlands, running Xray
- **Protocol** — VLESS + Reality (primary), Hysteria2 (UDP fallback, high throughput)
- **Watchdog** — `mihomo-watchdog.sh` monitors the process and restarts it on failure (via systemd)

## Features

- Transparent proxy — all LAN devices route automatically, no per-device setup
- Split routing — local/regional resources go direct, everything else through the proxy
- DNS over HTTPS — protects DNS queries from inspection/spoofing
- IPv4 + IPv6 support
- Automatic fallback to direct connection if the proxy is unreachable

## Configuration

| Parameter | Value |
|-----------|-------|
| Service | systemd |
| Config | `/etc/mihomo/config.yaml` |
| Web UI | `http://localhost:9090` |
| Autostart | `systemctl enable mihomo` |

> The config file itself is not included in this repo — it contains private data (server IP, auth keys).

## Debugging notes

Real-world issues solved while running this setup:
- DNS resolution failures under specific routing rules — traced to conflicting DNS-over-HTTPS and local resolver priority
- SNI-based blocking countermeasures — switched fronting domains and adjusted TLS fingerprinting
- Mode switching between transparent proxy and rule-based modes without dropping active connections
