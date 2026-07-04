#!/bin/bash
#Проверяет статус Docker-контейнеров на  по SSH

REMOTE_HOST="engine"
SERVICES="jellyfin prowlarr qbittorrent uptime-kuma grafana prometheus node_exporter"

check_service() {
    local service_name=$1
    local status
    status=$(ssh "$REMOTE_HOST" "docker ps | grep $service_name")

    if [ -n "$status" ]; then
        echo "✅ $service_name работает"
    else
        echo "❌ $service_name упал"
    fi
}

for service in $SERVICES; do
    check_service "$service"
done
