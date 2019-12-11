#!/usr/bin/make -f
# -*- mode:makefile -*-

json_1 := {"canciones": [{"name":"Cancion Server 1", "hash":"95678123"}]}
json_2 := {"canciones": [{"name":"Cancion Server 2", "hash":"sdfugy6"}]}

clean:
	$(info Borrando archivos innecesarios...)
	$(RM) -r /tmp/server2
	$(RM) -r __pycache__/
	$(RM) -r file_list.json
	$(RM) -r ./*.mp3

run:
	$(MAKE) app-workspace & sleep 1
	$(MAKE) run-icestorm &
	sleep 2
	$(MAKE) run-server1 &
	sleep 5
	$(MAKE) run-server2 &
	sleep 2
	$(MAKE) run-client

server-test:clean
	$(MAKE) app-workspace & sleep 1
	$(MAKE) run-icestorm &
	sleep 2
	$(MAKE) run-server1 &
	sleep 5
	$(MAKE) run-server2 &
	sleep 5
	cat file_list.json
	cat /tmp/server2/file_list.json

run-icestorm:
	$(info Ejecutando IceStorm...)
	gnome-terminal -- bash -c \
	"sh run_icestorm.sh; bash"

run-server1:
	$(info Ejecutando Servidor Nº1...)
	gnome-terminal -- bash -c \
	"cd /home/edulcorante/Escritorio/Practicas/DISTRIBUIDOS/practicaYoutube/AlfonsoGarcia/  && ./run_server.sh; bash"

run-server2:
	$(info Ejecutando Servidor Nº2...)
	gnome-terminal -- bash -c \
	"cd /tmp/server2/  && ./run_server.sh; bash"

run-client:
	$(info Ejecutando Cliente...)
	gnome-terminal -- bash -c \
	"echo 'Consola del cliente. Uso: ./run_client <proxy> <url>'; bash"

app-workspace:
	$(info Creando workspace)
	mkdir -p /tmp/server2/
	mkdir -p IceStorm/
	cp downloader.py server.config orchestrator.py run_server.sh TrawlNet.ice utiles.py  /tmp/server2/
	touch file_list.json
	echo '${json_1}' > file_list.json
	touch /tmp/server2/file_list.json
	echo '${json_2}' > /tmp/server2/file_list.json
	chmod 775 ./*
