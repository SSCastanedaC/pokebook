# pokebook

El proyecto ha sido desarrollando utilizando las siguientes especificaciones técnicas: <br>
<ul>
<li>Python 3.6.2</li>
<li>Django 2.2</li>
<li>Postgres 12.5</li>
</ul>

El proyecto se ha desplegado a un servidor de pruebas en Heroku. Para acceder al proyecto ingresar a: <br>
https://pokebookmo.herokuapp.com/ <br>
<italic>
*Debido a que se está utilizando un servidor de pruebas, la primera carga del sitio puede ser demorada ya que los dynos entran a estado de hibernación después de 30min de inactividad*
</italic>

Para consultar las cadenas de evolución ingresar a:<br>
https://pokebookmo.herokuapp.com/evolution-chain

Igualmente, se ha desarrollado una API tipo REST para consultar los pokemones con nombre con la siguiente especificación: <br>
<ul>
  <li>URI: https://pokebookmo.herokuapp.com/api/search_pokemon</li>
  <li>Método: POST</li>
  <li>Parámetros de Entrada:
    <ul>
      <li>Nombre: name</li>
      <li>Tipo: String</li>
    </ul>
</ul>
<br>    
La DB ha sido instanciada únicamente con las 3 primeras cadenas de evolución y los respectivos pokemones que pertenecen a ella.
<br>
En caso de clonar y ejecutar el proyecto de manera local, es necesario crear la extensión pg_trgm en Postgres ejecutando: <br>
CREATE EXTENSION pg_trgm;


