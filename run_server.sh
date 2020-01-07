#!/bin/sh
#

PYTHON=python3

DOWNLOADER_CONFIG=server.config
ORCHESTRATOR_CONFIG=$DOWNLOADER_CONFIG

PRX=$(tempfile)
$PYTHON downloader_factory.py --Ice.Config=$DOWNLOADER_CONFIG>$PRX &
PID=$!

# Dejamos arrancar al downloader
sleep 1
echo "Downloader: $(cat $PRX)"

PRX_TRANSFER=$(tempfile)
$PYTHON transfer_factory.py --Ice.Config=$DOWNLOADER_CONFIG>$PRX_TRANSFER &
PID_TRANSFER=$!

# Dejamos arrancar al downloader
sleep 1
echo "TRANSFER: $(cat $PRX_TRANSFER)"

# Lanzamos el orchestrator
$PYTHON orchestrator.py --Ice.Config=$ORCHESTRATOR_CONFIG "$(cat $PRX)" "$(cat $PRX_TRANSFER)"

echo "Shoutting down..."
kill -KILL $PID
rm $PRX
kill -KILL $PID_TRANSFER
rm $PRX_TRANSFER
