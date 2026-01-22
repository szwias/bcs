#!/usr/bin/env bash
cd /home/ubuntu/src || exit
docker-compose up -d
IP=$(hostname -I | awk '{print $1}')
echo "BCS Dashboard: http://$IP:8000/dashboard/"
