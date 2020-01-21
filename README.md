  [Repositorio Practica L3](https://github.com/luciaagarcia/AlfonsoGarcia/tree/L3)
---
 * Lucía Alfonso García
 * Eduardo García Aparicio

## Lanzamiento del sistema
Para lanzar correctamente el sistema correctamente deberemos situarnos
en el directorio raiz del proyecto y abrir una terminal.

#### Crear los nodos
A continuacion, tenemos dos opciones para lanzar los nodos de la 
aplicacion, crear los directorios correspondientes y aplicar
correctamente icepatch2calc.

Opciones disponibles:
```
$ ./run_server.sh
```
```
$ make run
```

#### Iniciar IceGridgui
Una vez lanzados los nodos, podremos lanzar el programa IceGridgui
para poder cargar la aplicacion y monitorizar el estado del sistema
ejecutando en una terminal el siguiente comando.
```
$ icegridgui
```
#### Conectarse al registro
Deberemos conectarnos al registro que previamente hemos lanzado.
Para ello, dentro de IceGridgui, haremos click en:
```
File → Login... → New Connection → Next → Next
```
Si hemos hecho todo bien, nos aparecera la opcion de conectarnos
al siguiente registro:
```
tcp -h <direccion ip> -p 10000 -t 60000
```
Lo seleccionamos, introducimos un usuario y una clave, pulsamos el
boton `Finish` y ya estaremos conectados al registro.

#### Cargar la aplicación
Cuando establezcamos la conexion con el registro, tendremos
que cargar la aplicacion YoutubeDownloaderApp en el regitro.

Para ello, primero abriremos la aplicacion YoutubeDownloaderApp.xml, la 
cual esta en el directorio raiz del proyecto, con icegridgui haciendo 
click en:
```
File → Open... → Application from file
```
Entonces nos aparecera un dialog donde deberemos seleccionar `YoutubeDownloaderApp.xml`

#### Poner en marcha la aplicación
Una vez cargada la aplicacion, solo nos quedara guardarla en el registro.

Cuando ya la tengamos guardada, iremos a la pestaña de `Live Deployment`
distribuiremos la aplicacion haciendo click en:
```
Tools → Application → Patch Distribution
```
Nos aparecera la opcion de elegir qué aplicacion deseamos distribuir, y pues como
queremos distribuir `YoutubeDownloaderApp` (será la unica que haya disponible), pulsamos
el boton `Aceptar` y ya tendremos la aplicacion lista para funcionar.

#### Descarga de canciones
Para ejecutar el cliente y asi poder hacer uso de la aplicación, iremos
al directorio raiz del proyecto, abriremos una terminal, y ejecutaremos uno
de los siguientes comandos:

```
$ ./run_client.sh
$ make run-client-download
$ make run-client-transfer
$ make run-client-list
```
 
Existe otra version de este manual, mas completo y con imagenes, disponible en [este enlace](https://github.com/luciaagarcia/AlfonsoGarcia/blob/L3/L3%20-%20AlfonsoGarcia.pdf)
