'''
URL params --> URL itself
Query params --> Everything after the ? in the URL
'''
import requests
from datetime import datetime
from PIL import Image
import numpy as np

ngrokurl = "http://f4f50a3c0e21.ngrok.io"
def get_data_inventory():
	call = requests.get("http://localhost:8001/info/", params={"shopid":100, "productid":100})
	print(call.json())

def post_data_inventory():
	contents = {
		"shopid":"S_061",
		"productid":"P_051",
		"quantity":123,
		"timestamp":datetime.now().strftime("%d-%M-%Y %H:%M:%S"),
		"alert":"Stock empty",
		"alert_type":0
				}
	call = requests.post("http://localhost:8001/info/", json=contents)
	print(call.json())

def get_data_emotion_model():
    call = requests.get(ngrokurl+"/modelsummary")
    print(call.json())

def post_data_emotion_model():
    #Conversion to RGB is needed as image is loaded with 4 channels RGBA format, converted to 3 channel RGB format
    image = Image.open("images/theflash.jpg", mode='r').convert("RGB").resize((48,48))
    image = np.asarray(image).astype("float64")
    print(image.shape)
    image = np.mean(image, axis=2)
    image = image/255.0
    print(image.shape)
    print(image)
    body = {"image":image.tolist()}
    call = requests.post(ngrokurl+"/predict", json=body)
    print(call.json())

get_data_inventory()
post_data_inventory()

#get_data_emotion_model()
#post_data_emotion_model()