from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import math
import csv
import io
from pandas import DataFrame
import pickle as p
import json
from scipy.ndimage import gaussian_filter1d


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
    print(data)
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
    sigma = 3
    data = request.get_json()
    print(data)
    accelerometer_data = data["accels"]
    rms_data = []
    for el in accelerometer_data:
        rms_data.append(math.sqrt( pow(el['x'],2) + pow(el['y'],2) + pow(el['z'],2) ))
    gaussian_data = gaussian_filter1d(rms_data,sigma)
    fft_data_real = np.fft.fft(gaussian_data).real.tolist()
    fft_data_imag = np.fft.fft(gaussian_data).imag.tolist()
    fft_data_mod = []
    for i in range(len(fft_data_real)):
        fft_data_mod.append(math.sqrt(pow(fft_data_real[i],2) + pow(fft_data_imag[i],2)))
    fft_data_mod = fft_data_mod[:16]
    data_consult = []
    data_consult.append(data["genero"])
    data_consult.append(data["edad"])
    for el in fft_data_mod:
        data_consult.append(el)
    pd_consult = DataFrame([data_consult],columns=["GENERO","EDAD","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13","A14","A15","A16"])
    prediction = model.predict(pd_consult)
    pred = int(np.array2string(prediction)[1])
    ans
    if pred == 0:
        ans = "Sentado"
    if pred == 1:
        ans = "Sentado"
    if pred == 2:
        ans = "Sentado"
    if pred == 3:
        ans = "Sentado"
    return jsonify(actividad="sentado")

if __name__ == '__main__':
    modelfile = 'models/final_prediction.pickle'
    model = p.load(open(modelfile,'rb'))
    app.run(debug= True, host='0.0.0.0')