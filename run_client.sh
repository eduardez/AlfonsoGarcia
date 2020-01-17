#!/bin/sh
#

echo "Downloading audio..."
./client.py --download "https://www.youtube.com/watch?v=9Meg1-O2k5Q" \
--Ice.Config=client.config

echo ""
echo "List request..."
./client.py --Ice.Config=client.config

echo ""
echo "Init transfer..."
./client.py --transfer "Poseidón" \
--Ice.Config=client.config