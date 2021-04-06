from flask import Flask, jsonify, abort,make_response,send_file,render_template
from flask_cors import CORS
import json
from time import time
import requests

URL_SWAPI_DEV = "https://swapi.dev/api/people/1"
# ------- Iniciacion de aplicacion Flask
app = Flask(__name__)
cors = CORS(app, resources={r"/gpon/*": {"origins": "*"}})

@app.route("/character/", methods=['GET'])
def get_character():
    try:
        response = requests.get(URL_SWAPI_DEV)
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
        
        basic_info["homeworld"] = home_world_info
        basic_info["species_name"] = species_name
        print (basic_info)
        return make_response(jsonify({'name': basic_info["name"]}), 200)
    except Exception as e:
        print (e)
        return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/character/rating/", methods=['POST'])
def set_character_rating ():
    
    pass

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# -------------------------------------- START ERROR HANDLES ROUTES BLOCK ---------------------------------
#----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	app.run(debug=True)

