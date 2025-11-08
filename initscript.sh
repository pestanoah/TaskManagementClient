#!/bin/sh

cd /home/pi/client
git pull origin main
sudo .venv/bin/python3.13 main.py