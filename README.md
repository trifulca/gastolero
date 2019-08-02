# Gastolero

## Motivación
Tenía ganas

## Levantar el proyecto

Para poner en funcionamiento el sistema se requiere `python 3.7.3` y `virtualenv`.

### Inicializar virtualenv
Una vez dentro del `virtualenv` se deben instalar los requerimientos para desarrollo de la siguiente manera:

```
$ ls
docs.txt  gastolero  README.md  requirements  requirements.txt  var
$ pip install -r requirements/local.txt
...
```

### Inicializar proyecto
Se debe ingresar en el proyecto Django, crear un settings local (para redefinir, o no, las variables que gusten) y definirlo como variable de entorno (?)

```
$ ls
docs.txt  gastolero  README.md  requirements  requirements.txt  var

$ cd gastolero/
$ echo 'from settings.base import *' > settings/local.py
$ export DJANGO_SETTINGS_MODULE=settings.local
$ ./manage.py runserver
```
