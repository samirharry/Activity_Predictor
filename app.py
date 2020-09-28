from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import csv
import io
import pickle as p
import json


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/',methods=['POST'])
@cross_origin()
def makecalc():
    data = request.get_json()
    prediction = np.array2string(model.predict(data))
    return jsonify(prediction)


@app.route('/api/save',methods=['POST'])
@cross_origin()
def savedata():
    raw_data_x_filename = 'data/raw_data_x.csv'
    raw_data_y_filename = 'data/raw_data_y.csv'
    raw_data_z_filename = 'data/raw_data_z.csv'
    data = request.get_json()
    accelerometer_data = data["accels"]
    len_data = len(accelerometer_data)
    print(len_data)
    len_file = 0
    with open(raw_data_x_filename,newline='') as File:
        reader = csv.reader(File,dialect='excel')
        for row in reader:
            len_file = len_file +1
    newid = 1+ (len_file-1)//len_data
    print(data)
    ## Almacenando los datos del eje x
    with open(raw_data_x_filename,'a',newline='') as File:
        writer = csv.writer(File,dialect='excel')
        for i in range(len_data):
            writer.writerow([newid,data["genero"],data["edad"],i,data["accels"][i]["x"],data["actividad"]])
    ## Almacenando los datos del eje y
    with open(raw_data_y_filename,'a',newline='') as File:
        writer = csv.writer(File,dialect='excel')
        for i in range(len_data):
            writer.writerow([newid,data["genero"],data["edad"],i,data["accels"][i]["y"],data["actividad"]])
    ## Almacenando los datos del eje z
    with open(raw_data_z_filename,'a',newline='') as File:
        writer = csv.writer(File,dialect='excel')
        for i in range(len_data):
            writer.writerow([newid,data["genero"],data["edad"],i,data["accels"][i]["z"],data["actividad"]])
    return jsonify("ok")

@app.route('/api/guess',methods=['POST'])
@cross_origin()
def makerequest():
    data = request.get_json()
    accelerometer_data = data["accels"]
    len_data = len(accelerometer_data)  
    for i in range(len_data):
        print(accelerometer_data[0]["x"])
        print(accelerometer_data[0]["y"])
        print(accelerometer_data[0]["z"])
    return jsonify(data)

if __name__ == '__main__':
    modelfile = 'models/final_prediction.pickle'
    model = p.load(open(modelfile,'rb'))
    app.run(debug= True, host='0.0.0.0')