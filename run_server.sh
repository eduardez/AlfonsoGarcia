gnome-terminal -- bash -c \
"python3 Downloader.py --Ice.Config=downloader.config | tee proxy.out; bash"

var=$(head -n 1 proxy.out)
echo "$var"
PID = $!

sleep 1
gnome-terminal -- bash -c \
"python3 Orchestrator.py --Ice.Config=orchestrator.config; bash"

kill -kill $PID
