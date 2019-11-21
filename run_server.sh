
python3 Downloader.py --Ice.Config=downloader.config | tee proxy.out &

PID=$!

echo $PID

sleep 1

clear

python3 Orchestrator1.py --Ice.Config=orchestrator.config

kill -kill $PID
