from flask import Flask, jsonify, abort,make_response,send_file,render_template
from flask_cors import CORS
import json
from time import time
import requests
import sqlite3


URL_SWAPI_DEV = "https://swapi.dev/api/people/"
# ------- Iniciacion de aplicacion Flask
app = Flask(__name__)
cors = CORS(app, resources={r"/gpon/*": {"origins": "*"}})
con = sqlite3.connect('characters.db')


# Create table
try:
    cur = con.cursor()
    cur.execute('''CREATE TABLE ratings
               (id integer, rating integer)''')
    con.close()
except: # ver si la excepcion es porque ya eexite
    pass

@app.route("/character/<string:id>", methods=['GET'])
def get_character(id):
    try:
        # recibir el id en los params porque el enunciado marca la url de la api sin id
        # comprobar que sea un numero el id
        # concatenar bien!
        
        url_api = URL_SWAPI_DEV + str(id)
        response = requests.get(url_api)
        basic_info = response.json()
        
        home_world = requests.get(basic_info["homeworld"]).json()
        home_world_info = { "name": home_world["name"], 
                            "population": home_world["population"], 
                            "known_residents_counts": len(home_world["residents"])
                          }
        if len (basic_info["species"]):
            species = requests.get(basic_info["species"][0]).json()
            species_name = species["name"]
        else:
            species_name = ""
        # consultar avg y max ratings de ese character. Si no trae nada ver que devolver
        average_rating = 0
        max_rating = 0
        basic_info["homeworld"] = home_world_info
        basic_info["species_name"] = species_name
        print (basic_info)
        data_response = {
            "name": basic_info["name"],
            "height": basic_info["height"],
            "mass": basic_info["mass"],
            "hair_color": basic_info["hair_color"],
            "skin_color": basic_info["skin_color"],
            "eye_color": basic_info["eye_color"],
            "birth_year": basic_info["birth_year"],
            "gender": basic_info["gender"],
            "homeworld": home_world_info,
            "species_name": species_name,
            "average_rating": average_rating,
            "max_rating": max_rating
        }
        return make_response(jsonify(data_response), 200)
    except Exception as e:
        print (e)
        return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/character/rating/", methods=['POST'])
def set_character_rating ():
    con = sqlite3.connect('characters.db')
    cur = con.cursor()
    data_character = (int(id), basic_info["name"], basic_info["height"], basic_info["mass"], basic_info["hair_color"], basic_info["skin_color"], basic_info["eye_color"],
                            basic_info["birth_year"], basic_info["gender"], home_world_info["name"], home_world_info["population"], home_world_info["known_residents_counts"],
                            species_name, 0, 0)
    cur.execute('INSERT INTO characters VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data_character)
    con.commit()
    con.close()
    pass

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# -------------------------------------- START ERROR HANDLES ROUTES BLOCK ---------------------------------
#----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	app.run(debug=True)

