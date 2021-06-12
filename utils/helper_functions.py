import pandas as pd
import re
from markupsafe import escape

def search_inventory(shopid, productid):
	inventory = pd.read_csv("database/my_inventory.csv", index_col=["productid", "shopid"]) 
	#We define a multi index
	try:
		quantity = int(inventory.loc[productid].loc[shopid].values[0])
	except:
		quantity = "Invalid input"
	response_data = {
			"ShopID":escape(shopid), 
			"ProductID":escape(productid), 
			"Quantity(Units)": quantity
					}
	return response_data


def search_inv_form_params(dict_of_params):
	inventory = pd.read_csv("database/my_inventory.csv")
	print(dict_of_params)
	data = {}
	try:
		for key, value in dict_of_params.items():
			print("Key=", key, "\tValue=",value)
			if(value!=""):
				if(key == "quantity"):
					value = int(value)
				inventory = inventory[inventory[key]==value]
		if(len(inventory)>0):
			data = inventory.to_dict(orient="records")
		else:
			data = {"Message": "No data matching all criteria"}	
	except:
		data = {"Message": "No data matching all criteria"}
	print("DATA AFTER FILTERING: ", data)
	return data

def check_input(dict_of_params):
	'''
	Check if each param for the keys are in valid format, like shopid must have form S_ followed by some numbers, quantity can be 0 OR any number not starting with a zero. Different cases: no match found (len == 0) or multiple matches (len > 1) or matched for a part (all_matches[0]!=value) like S_011lucky is invalid. return 0 for any invalid format else return -1
	'''
	flag = -1
	valid_formats = {
			"shopid":r"S_[0-9]+",
			"productid":r"P_[0-9]+",
			"quantity":r"0|[1-9][0-9]*"
	}
	for key, value in dict_of_params.items():
		if(value!=""):
			all_matches = re.findall(valid_formats[key], value)
			if(len(all_matches)==0 or len(all_matches)>1 or all_matches[0]!=value):
				flag = 0
				break
	return flag


