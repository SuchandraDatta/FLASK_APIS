from flask import Flask, request, render_template, jsonify
from utils import helper_functions as hf
from utils import database as db
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
import sys
app = Flask(__name__, static_folder="static")
auth = HTTPBasicAuth()
'''conn = db.create_connection("database/Phoenix.db")
db.create_userinfo_table(conn)
print(db.view_table(conn))
conn.close()'''

@auth.verify_password
def verify_password(username, password):
	conn = db.create_connection("database/Phoenix.db")
	userinfo = db.view_table(conn)
	for item in userinfo:
		if(item[0] == username and check_password_hash(item[1], password) == True):
			return username


@app.route("/", methods=["GET"])
@auth.login_required
def index_page():
	return render_template("index.html", message="")


@app.route("/get_info", methods=["GET"])
@auth.login_required
def get_info():
	#Using request.args.get returns None instead of raising any key error	
	#Did the user select atleast one option ? If not show error message and reload the page
	if(any(list(request.args.values())) != True):
		return render_template("index.html", message="Please select at least one option")
	#Sanitize inputs, check if proper format using regex
	elif(hf.check_input(request.args)!= -1):
		return render_template("index.html", message="Please ensure correct values for shopid/productid/quantity")
	else:
		data = hf.search_inv_form_params(request.args)
		return render_template("output.html", data=data)












if __name__ == "__main__":
	app.run(host="localhost", port=8000, debug=True)