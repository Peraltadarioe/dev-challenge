# Star Wars API-Rest Python

## Instalación
   1. Instalar Python -> https://www.python.org/downloads/  
   2. Instalar librerías  
      - Desde la consola:  
          - pip install Flask  

## Rutas de API

### [GET] /character/

Parámetros  
id -> Id del personaje. Este valor se utiliza para consultar a https://swapi.dev/api/people  

Respuestas  

 Código 200  
 Ejemplo:  
 ```
  {  
    "average_rating": null,  
    "birth_year": "19BBY",  
    "eye_color": "blue",  
    "gender": "male",  
    "hair_color": "blond",  
    "height": "172",  
    "homeworld": {  
        "known_residents_counts": 10,  
        "name": "Tatooine",  
        "population": "200000"  
    },  
    "mass": "77",  
    "max_rating": null,  
    "name": "Luke Skywalker",  
    "skin_color": "fair",  
    "species_name": ""  
  }  
```

  Código 500  
  Ejemplo  
  ```
     {'state': 'Error interno'}  
  ```

### [POST] /character/rating/  

 Ejemplo POST body (json)  
 ```
   {  
     "id":1,  
     "rating": 5  
   }  
 ```


 Respuestas  

  Código 200  
  Ejemplo:  
     ```
     {"state": "ok"}  
     ```

  Código 500  
   Ejemplo
   ```  
    {"state": "Error al intentar guardar el rating"}  
   ```

  Código 400  
   Ejemplo
   ```  
    {"state": "Error en la petición"}  
   ```
