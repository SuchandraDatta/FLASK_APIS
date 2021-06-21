import pandas as pd
import json, sys
from utils import helper_functions as hf
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from csv import DictWriter
import configs as config
import os

app = Flask(__name__)
swaggerui_blueprint = get_swaggerui_blueprint(
    config.SERVER_SETTINGS.get("SWAGGER_URL"),
    config.SERVER_SETTINGS.get("SWAGGER_API_URL"),
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    })
app.register_blueprint(swaggerui_blueprint)
@app.route('/', methods=["GET"])
def index_page():
	return "INDEX PAGE"

@app.route('/info/<string:shopid>/<string:productid>', methods=["GET"])
def get_info(shopid, productid):
	'''
	Return response(shopid, productid, quantity in inventory) from known parameters in URL
	'''
	return jsonify(hf.search_inventory(shopid, productid))

@app.route('/info/', methods=["POST"])
def save_info():
	'''
	Return response and save alert messages to CSV
	'''
	status_message = ""
	try:
		data_dict = json.loads(request.data)
		print(data_dict, file=sys.stderr)
		#The newline if not specified makes extra empty rows appear as windows translates \n as \r\n and csv writes a \r\n so if not opened in binary mode, \r\n is interpreted as \r\n\n.. Windows specific thing
		with open("database/alert_messages.csv", "a", newline="") as file:
			dw = DictWriter(file, fieldnames = list(data_dict.keys()))
			dw.writerow(data_dict)
		status_message = "Message saved"
	except:
		status_message = "Error, please try again later"
	return jsonify({"Status":status_message})

@app.route('/info/', methods=["GET"])
def get_info_query_params():
	'''
	Return response(shopid, productid, quantity) from query parameters
	'''
	shopid = int(request.args.get("shopid"))
	productid = int(request.args.get("productid"))
	return jsonify(hf.search_inventory(shopid, productid))
	

#Flask class, instance of this class is the WSGI application.__name__ says if app is started as an application __name__ == main or as a module in which case name would be name of the module.
#route() decorator to say which URL to listen to. Give URL rule as string, endpoint that Flask assumes to be name of the view function and options, which specifies which methods are allowed GET, POST etc.
'''
request.args == query params
request.form == HTML form data
request.files == files from form HTML
request.json == when application/json is there
request.data == raw data if it couldnt get parsed as HTML form data
All of these are multidict instances except for json, access them like request.form["hey"] or if you dont know if the key exists use request.form.get("hey")
'''
PORT = int(os.environ.get("PORT", config.SERVER_SETTINGS.get("PORT")))
if __name__ == "__main__":
	app.run(host="localhost", port=PORT, debug=True)