#!/bin/sh
#

echo "Downloading audio..."
./client.py --download "https://vimeo.com/383001078" \
--Ice.Config=client.config

echo ""
echo "List request..."
./client.py --Ice.Config=client.config

echo ""
echo "Init transfer..."
./client.py --transfer "The Blank Page" \
--Ice.Config=client.config