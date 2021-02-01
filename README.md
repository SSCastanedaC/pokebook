# pokebook

El proyecto ha sido desarrollando utilizando las siguientes especificaciones técnicas:
Python 3.6.2
Django 2.2
Postgres 12.5

El proyecto se ha desplegado a un servidor de pruebas en Heroku. Para acceder al proyecto ingresar a:
https://pokebookmo.herokuapp.com/
*Debido a que se está utilizando un servidor de pruebas, la primera carga del sitio puede ser demorada ya que los dynos entran a estado de hibernación después de 30min de inactividad

Para consultar las cadenas de evolución ingresar a:
https://pokebookmo.herokuapp.com/evolution-chain

Igualmente, se ha desarrollado una API tipo REST para consultar los pokemones con nombre con la siguiente especificación:
  URI: https://pokebookmo.herokuapp.com/api/search_pokemon
  Método: POST
  Parámetros de Entrada:
    -Nombre: name
    -Tipo: String
    
La DB ha sido instanciada únicamente con las 3 primeras cadenas de evolución y los respectivos pokemones que pertenecen a ella.

En caso de clonar y ejecutar el proyecto de manera local, es necesario crear la extensión pg_trgm en Postgres ejecutando:
CREATE EXTENSION pg_trgm;


