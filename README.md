# GRUPO6-2024-PROYINF
## Integrantes: 
- Eduardo Rodríguez 202273593-7
- Sebastián Huerta 202273590-2
- Sebastián Muñoz 202273534-1
- Sebastián Olea 202273566-K<br/>
## Video de la presentacion del cliente: 
- Puedes ver la presentacion [aqui][video]

[video]: https://www.youtube.com/watch?v=abJau21SDIk

## Video de los resultados finales: 
- Puedes ver el video [aqui][a]

[a]: https://www.youtube.com/watch?v=Tnv5N3LQiko

## Wiki
- Puede acceder a la Wiki desde el siguiente [enlace][link]

[link]: https://github.com/asecino32/GRUPO6-2024-PROYINF/wiki

## Instrucciones Página

Modificar el archivo que está en `ProyA/analisis/settings.py`, en la sección que dice `TEMPLATES` para que coincidan los datos del usuario de PostgreSQL, o modificar las credenciales del usuario de PostgreSQL para que coincidan con las del archivo. Luego, crear una base de datos llamada `documentos` en PostgreSQL. Esto se puede hacer mediante los siguientes comandos:

```bash
# Primero, acceder a la dirección del bin de la versión de PostgreSQL
cd "C:\Program Files\PostgreSQL\*numero de la versión de postgres instalada*\bin"

# Luego, ejecutar la consola (los paréntesis no van)
psql -U (postgres o el nombre de usuario que le haya puesto)

# Si quiere cambiar la contraseña del usuario use el siguiente comando (la nueva contraseña debe ir entre comillas)
ALTER USER nombre_usuario WITH PASSWORD 'nueva_contraseña';

# Finalmente, crear la base de datos "documentos"
CREATE DATABASE documentos;


# En la terminal de Visual Studio Code, navegar hasta la carpeta ProyA (por ejemplo, ../ProyA) y ejecutar los siguientes comandos:
py manage.py migrate  # Realizar las migraciones
py manage.py runserver  # Ejecutar el servidor
```
# GRUPO19-2025-1-PROYINF
## Integrantes (se mantienen del semestre anterior): 
- Eduardo Rodríguez 202273593-7
- Sebastián Huerta 202273590-2
- Sebastián Muñoz 202273534-1
- Sebastián Olea 202273566-K<br/>

## Proyecto a continuar:
Se continuara trabajando en este repositorio, el mismo proyecto del semestre anterior
