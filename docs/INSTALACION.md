# Instalación y Configuración

## Sin Docker
Requisitos:
- Tener instalado Python 3.11.0 o superior.
- Tener instalado PIP 22.0.0 o superior (Package Manager).

Pasos a seguir:
- Abrir una terminal de comandos de Windows.
- Ir a la carpeta source de este repositorio (src), donde se encuentra el archivo requirements.txt
- Ejecutar => pip install -r requirements.txt
- Ejecutar => python api.py
- Verificar si la aplicacion quedo en ejecución visitando en su navegador de preferencia el siguiente enlace: http://127.0.0.1:5000/
- Si puede ver la pagina web anteriormente mencionada, ya puede usar los endpoints que se encuentran en la misma. También puede hacer uso de la colección de postman ubicada en docs/postman.
- En cualquier momento se podra hacer uso de Ctrl+C para terminar la ejecución de la API.


## Con Docker
Requisitos:
- Tener instalado Docker CLI (Command Line Interface).
- Tener activo el servicio de docker.

Pasos a seguir:
- Abrir una terminal de comandos de Windows.
- Ir a la carpeta root de este repositorio, donde se encuentra el Dockerfile.
- Ejecutar => docker build -t nosql:1.0.0-api .
- Esperar a que descargue la imagen de python y se cree una nueva llamada "nosql:1.0.0-api".
- Elegir una de las formas de ejecutar la imagen del docker.
- A) Ejecutar de forma interactiva => docker run -it -p 5555:5000 nosql:1.0.0-api
- B) Ejecutar en el background => docker run -d -p 5555:5000 nosql:1.0.0-api
- Verificar si la aplicacion quedo en ejecución visitando en su navegador de preferencia el siguiente enlace: http://127.0.0.1:5555/
- Si puede ver la pagina web anteriormente mencionada, ya puede usar los endpoints que se encuentran en la misma. También puede hacer uso de la colección de postman ubicada en docs/postman.
- A) Si el contenedor fue ejecutado de forma interactiva, se podrá hacer uso de Ctrl+C para terminar la ejecución de la API.
- B) Si el contenedor está siendo ejecutado en el background, se debera usar un comando de docker para apagarlo.
- B1) Conseguir el ID del contenedor. Ejecutar => docker ps
- B2) Si el contenedor está siendo ejecutado en el background, se debera usar un comando de docker para apagarlo. Ejecutar => docker stop ContenedorID