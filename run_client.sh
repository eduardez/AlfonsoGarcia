#!/bin/sh
#

echo "Downloading audio..."
./client.py --download "https://www.youtube.com/watch?v=PaFnO5LKTSs" \
--Ice.Config=client.config

echo ""
echo "List request..."
./client.py --Ice.Config=client.config

echo ""
echo "Init transfer..."
./client.py --transfer "Spiderman" \
--Ice.Config=client.config