./dowloader.py --Ice.Config=downloader.Config | tee proxy.out &
var=$(head -n 1 proxy.out)
echo "$var"
PID = $!


./orchestrator.py --Ice.Config=orchestrator.config "$var"

kill -kill $PID