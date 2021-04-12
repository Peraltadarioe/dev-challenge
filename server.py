#############################################################################################
# Tipo de archivo: Script Py
# Nombre: server.py
# Fecha: 12/04/2021
# Autor: Darío Peralta
# Contacto: peraltadarioe@gmail.com
# Version: V1.0
# Descripcion:  Api que permite consultar datos de personajes desde https://swapi.dev/ e insertar ratings para cada uno de ellos
#               Además calcula el rating máximo y el promedio de ratings para cada personaje
#############################################################################################

# ------- START IMPORTS BLOCK -------------------------------------------------------------------
from flask import Flask, request, jsonify,make_response
from flask_cors import CORS
import json
from time import time
import requests
import sqlite3
# ------- END IMPORTS BLOCK -------------------------------------------------------------------

# ------ FUNCTIONS ------------------------------------------------------------------------
def create_ratings_table():
    try:
        cur = con.cursor()
        cur.execute('''CREATE TABLE iF NOT EXISTS ratings
                (id integer, rating integer)''')
        con.close()
    except Exception as e:
        print (e)
# ------ FUNCTIONS ------------------------------------------------------------------------

# ------ START INIT BLOCK ---------------------------------------------------------------------
app = Flask(__name__)
cors = CORS(app, resources={r"/gpon/*": {"origins": "*"}})
con = sqlite3.connect('characters.db')
# ------ END INIT BLOCK -----------------------------------------------------------------------

# -------------------------------------- START API ENDPOINTS ---------------------------------
# Recibe el id del personaje y devuelve los datos requeridos
# Para ello consulta a la api y calcula los ratings guardados
# Si no existen ratings para el personaje devuelve null en los campos average y max
@app.route("/character/<string:id>", methods=['GET'])
def get_character(id):
    try:
        url_api = "https://swapi.dev/api/people/%s" % id
        # se consulta info general del personaje
        response = requests.get(url_api)
        basic_info = response.json()
        # se consulta la info de home_world
        home_world = requests.get(basic_info["homeworld"]).json()
        home_world_info = { "name": home_world["name"], 
                            "population": home_world["population"], 
                            "known_residents_counts": len(home_world["residents"])
                          }
        # se consulta la info de species
        if len (basic_info["species"]):
            species = requests.get(basic_info["species"][0]).json()
            species_name = species["name"]
        else:
            species_name = ""
        # Se consulta a la db los ratings del personale
        average_rating = None
        max_rating = None
        ratings = []
        con = sqlite3.connect('characters.db')
        cur = con.cursor()
        query_id = (int(id),)
        # Si existen ratings se calcula el avg y el max
        for row in cur.execute('SELECT * FROM ratings WHERE id=?', query_id):
            ratings.append(row[1])
        con.close()
        if len(ratings) > 0:
            average_rating = sum(ratings) / len(ratings)
            max_rating = max(ratings)
        # Se arma la estructura de datos requerida para el response
        data_response= {"name": basic_info["name"], "height": basic_info["height"], "mass": basic_info["mass"],
                        "hair_color": basic_info["hair_color"], "skin_color": basic_info["skin_color"], "eye_color": basic_info["eye_color"],
                        "birth_year": basic_info["birth_year"], "gender": basic_info["gender"], "homeworld": home_world_info,
                        "species_name": species_name, "average_rating": average_rating, "max_rating": max_rating
        }
        return make_response(jsonify(data_response), 200)
    except Exception as e:
        print (e)
        return make_response(jsonify({'state': 'Error interno'}), 500)

# Ruta que recibe el id del personaje y un rating
# Se guarda en la base de datos
@app.route("/character/rating/", methods=['POST'])
def set_character_rating ():
    data = request.json
    try:
        con = sqlite3.connect('characters.db')
        cur = con.cursor()
        cur.execute('INSERT INTO ratings VALUES (?,?)', (data["id"], data["rating"]))
        con.commit()
        con.close()
        return make_response(jsonify({"state": "ok"}), 200)
    except Exception as e:
        print (e)
        return make_response(jsonify({"state": "Error al intentar guardar el rating"}), 500)
    # -------------------------------------- END API ENDPOINTS ---------------------------------

# -------------------------------------- START ERROR HANDLES ROUTES BLOCK ---------------------------------
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'state': 'Not found'}), 404)
# -------------------------------------- END ERROR HANDLES ROUTES BLOCK ---------------------------------

if __name__ == '__main__':
    create_ratings_table()
    app.run(debug=True)

