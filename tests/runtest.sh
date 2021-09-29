#!/bin/sh
docker-compose down 
echo 'y' | docker volume prune 
docker-compose up -d
sleep 10
cd $(dirname $(stat -f "$0"))
cd backend
python3 authentication.py 
python3 message.py