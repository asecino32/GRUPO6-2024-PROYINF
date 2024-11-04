# GRUPO6-2024-PROYINF
## Integrantes: 
- Eduardo Rodríguez 202273593-7
- Sebastián Huerta 202273590-2
- Sebastián Muñoz 202273534-1
- Sebastián Olea 202273566-K<br/>
## Video de la presentacion del cliente: 
- Puedes ver la presentacion [aqui][video]

[video]: https://www.youtube.com/watch?v=abJau21SDIk

## Wiki
- Puede acceder a la Wiki desde el siguiente [enlace][link]

[link]: https://github.com/asecino32/GRUPO6-2024-PROYINF/wiki

## Instrucciones Pagina
Modificar el archivo que está en ProyA/análisis/settings.py, la sección que dice “TEMPLATES” para que coincidan los datos del usuario postgres o modificar las credenciales del usuario de postgres para que coincidan con las del archivo, luego crear una base de datos llamada “documentos” en postgres, esto se puede hacer mediante los siguientes comandos: <br/>
//primero acceder a la dirección del bin de la versión de postgres<br/>
cd "C:\Program Files\PostgreSQL\*numero de la versión de postgres instalada*\bin"<br/>
//luego ejecutar la consola los () no van<br/>
psql -U (postgres o el nombre de usuario que le haya puesto) <br/>
//si quiere cambiar la contraseña del usuario use el siguiente comando, la nueva contraseña debe ir entre comillas<br/>
ALTER USER nombre_usuario WITH PASSWORD 'nueva_contraseña'; <br/>
//finalmente crear la base de datos documentos <br/>
CREATE DATABASE documentos; <br/>
luego en la terminal de visual navegar hasta donde este la carpeta ProyA, para que quede ../ProyA y usar el comando py manage.py migrate, luego el py manage.py runserver <br/>
