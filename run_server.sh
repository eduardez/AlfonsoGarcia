python3 Downloader.py --Ice.Config=server.config | tee proxy.out &

PID=$!
echo $PID

sleep 1

clear

python3 Orchestrator1.py --Ice.Config=server.config

kill -kill $PID
