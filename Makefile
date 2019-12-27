#!/usr/bin/make -f
# -*- mode:makefile -*-

# ---------------------------------------------------------------------------
# ---------------------     IMPORTANTE      ---------------------------------
#
# 		Para ejecutar bien el make en todo su esplendor, poner
#		la variable NUM_SERVERS al numero de servidores deseado.
#		
#		Si por algun casual quieres cambiar ese numero de servidores y/o
#		quieres reiniciar sus datos, utilizar re-run.
#
#				usage: run | re-run NUM_SERVERS=n
#
# ---------------------------------------------------------------------------

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
SERVER_BASEDIR_PATH := /tmp/server
NUM_SERVERS := 2
RANGE:=$(shell seq 1 $(NUM_SERVERS))
ARCHIVOS = downloader_factory.py server.config orchestrator.py run_server.sh trawlnet.ice utiles.py

all:



clean:
	$(info Borrando archivos innecesarios...)
	$(RM) -r /tmp/server*
	$(RM) -r __pycache__/
	$(RM) -r file_list.json
	$(RM) -r ./*.mp3

run:
	$(MAKE) server-workspace & 
	sleep 1
	$(MAKE) run-icestorm &
	sleep 2	
	$(MAKE) run-server &
	sleep 1
	$(MAKE) run-client

re-run:
	$(MAKE) clean
	$(MAKE) server-workspace & 
	sleep 1
	$(MAKE) run-icestorm &
	sleep 2	
	$(MAKE) run-server &
	sleep 1
	$(MAKE) run-client


run-icestorm:
	$(info Ejecutando IceStorm...)
	gnome-terminal -- bash -c \
	"./run_icestorm.sh; bash"

run-server:
	$(info Ejecutando Servidores...)
#hay un pequeño problema con este metodo, y es que va a ejecutar los orquestadores de 
# TODAS las carpetas server, es decir, aunque pongas NUM_SERVERS = N, va a ejecutar
# tantos orquestadores como carpetas haya, por eso hay que ejecutar un make clean
	for f in /tmp/server*;\
		do \
		cd $${f};\
		pwd;\
		gnome-terminal -- bash -c "sh run_server.sh; bash" & sleep 2;\
	done;

run-client:
	$(info Ejecutando Cliente...)
	gnome-terminal -- bash -c \
	"echo 'Consola del cliente. Uso: ./run_client <proxy> <url>'; bash"

server-workspace:
#Crear los directorios
	$(foreach var,$(RANGE),mkdir -p $(SERVER_BASEDIR_PATH)$(var)) &
#Copiar los archivos
	cd $(shell dirname $(mkfile_path))
	$(foreach num_serv,$(RANGE),\
		$(foreach nombre_archivo,$(ARCHIVOS),\
			cp $(nombre_archivo) $(SERVER_BASEDIR_PATH)$(num_serv)/ &))
	chmod 775 /tmp/server*
	