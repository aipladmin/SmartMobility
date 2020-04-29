from flask import Flask,request,jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import requests
import json
application = app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/v1/jsondata/all')
def api():
	mlroutes = None
	mlroutes = {
	'success':True,
	'dataset1':{'description':'RBR','data':''},
	'dataset2':{'description':'WBW','data':''},
	'dataset3':{'description':'TW','data':''},
	'dataset4':{'description':'FW','data':''},
	}
	RBR = pd.read_csv('d1.csv')
	RBR = RBR.to_json(orient='records')


	WBR = pd.read_csv('d2.csv')
	WBR = WBR.to_json(orient='records')

	TW = pd.read_csv('d3.csv')
	TW = TW.to_json(orient='records')		

	FW = pd.read_csv('d4.csv')
	FW = FW.to_json(orient='records')			

	mlroutes['dataset1']['data'] = json.loads(RBR)
	mlroutes['dataset2']['data'] = json.loads(WBR)
	mlroutes['dataset3']['data'] = json.loads(TW)
	mlroutes['dataset4']['data'] = json.loads(FW)
	# print(type(mlroutes))
	# mljson = json.dumps(mlroutes)
	# print(type(mljson))
	mljson = open("mljson.json", "w") 
	json.dump(mlroutes, mljson, indent = 4) 
	mljson.close() 
	return "DATA"

@app.route('/api/v1/jsondata/cd/<string:day>/<string:time>',methods=['GET'])
def curated_data(day,time):
	cdjson = None
	cdjson={'success':True,
			'dataset1':{'description':'RBR','total_time':'','waiting_time':''},
			'dataset2':{'description':'WBW','data':'','waiting_time':''},
			'dataset3':{'description':'TW','data':''},
			'dataset4':{'description':'FW','data':''}
			}
	print(day,'          ',time)
	url = "https://raw.githubusercontent.com/madhavparikh99/SmartMobility/master/mljson.json"
	dapi = pd.read_json(url)
	dataset=dapi['dataset1']['data']
	x1 = [ xd['Day'] for xd in dataset ] 
	x2 = [ xd['Time Slots'] for xd in dataset ] 
	X = list(map(list,zip(x1,x2)))
	y = [ xy['Ttime'] for xy in dataset ] 
	y1 = []
	for i in y:
	    j=i.split(":")
	    y1.append((int(j[0])*60)+int(j[1]))
	X_train, X_test, y1_train, y1_test = train_test_split(X, y1, test_size = 1/3, random_state = 0)
	regressor = LinearRegression()
	regressor.fit(X_train, y1_train)
	y1_pred = regressor.predict(X_test)
	pickle.dump(regressor, open('model.pkl','wb'))
	model = pickle.load(open('model.pkl','rb'))
	a=model.predict([[int(day),int(time)]])
	#****************************************************************
	x1 = [ xd['Day'] for xd in dataset ] 
	x2 = [ xd['Time Slots'] for xd in dataset ] 
	X = list(map(list,zip(x1,x2)))
	y = [ xy['Wtime'] for xy in dataset ] 
	y2 = []
	for i in y:
	    j=i.split(":")
	    y2.append((int(j[0])*60)+int(j[1]))
	X_train, X_test, y2_train, y2_test = train_test_split(X, y2, test_size = 1/3, random_state = 0)
	regressor = LinearRegression()
	regressor.fit(X_train, y2_train)
	y2_pred = regressor.predict(X_test)
	pickle.dump(regressor, open('model.pkl','wb'))
	model = pickle.load(open('model.pkl','rb'))
	b=model.predict([[int(day),int(time)]])
	#****************************************************************
	print("Output 1:")
	a = (str(int(a//60))+":"+str(int(a%60))+":00")
	b = (str(int(b//60))+":"+str(int(b%60))+":00")
	print(a,'				',b)
	
	data = a
	ds = b
	cdjson['dataset1']['total_time'],cdjson['dataset1']['waiting_time'] =  data,ds
	
	dataset=dapi['dataset2']['data']
	x1 = [ xd['Day'] for xd in dataset ] 
	x2 = [ xd['Time Slots'] for xd in dataset ] 
	X = list(map(list,zip(x1,x2)))
	y = [ xy['Ttime'] for xy in dataset ] 
	y1 = []
	for i in y:
	    j=i.split(":")
	    y1.append((int(j[0])*60)+int(j[1]))
	X_train, X_test, y1_train, y1_test = train_test_split(X, y1, test_size = 1/3, random_state = 0)
	regressor = LinearRegression()
	regressor.fit(X_train, y1_train)
	y1_pred = regressor.predict(X_test)
	pickle.dump(regressor, open('model.pkl','wb'))
	model = pickle.load(open('model.pkl','rb'))
	a=model.predict([[int(day),int(time)]])
	#****************************************************************
	x1 = [ xd['Day'] for xd in dataset ] 
	x2 = [ xd['Time Slots'] for xd in dataset ] 
	X = list(map(list,zip(x1,x2)))
	y = [ xy['Wtime'] for xy in dataset ]
	y2 = []
	for i in y:
	    j=i.split(":")
	    y2.append((int(j[0])*60)+int(j[1]))
	X_train, X_test, y2_train, y2_test = train_test_split(X, y2, test_size = 1/3, random_state = 0)
	regressor = LinearRegression()
	regressor.fit(X_train, y2_train)
	y2_pred = regressor.predict(X_test)
	pickle.dump(regressor, open('model.pkl','wb'))
	model = pickle.load(open('model.pkl','rb'))
	b=model.predict([[int(day),int(time)]])
	#****************************************************************
	print("Output 2:")
	a = (str(int(a//60))+":"+str(int(a%60))+":00")
	b = (str(int(b//60))+":"+str(int(b%60))+":00")

	data = a
	ds = b
	cdjson['dataset2']['total_time'],cdjson['dataset2']['waiting_time'] =  data,ds

	print("\n")
	dataset=dapi['dataset3']['data']
	x1 = [ xd['Day'] for xd in dataset ] 
	x2 = [ xd['Time Slots'] for xd in dataset ] 
	X = list(map(list,zip(x1,x2)))
	y = [ xy['Ttime'] for xy in dataset ]
	y1 = []
	for i in y:
	    j=i.split(":")
	    y1.append((int(j[0])*60)+int(j[1]))
	X_train, X_test, y1_train, y1_test = train_test_split(X, y1, test_size = 1/3, random_state = 0)
	regressor = LinearRegression()
	regressor.fit(X_train, y1_train)
	y1_pred = regressor.predict(X_test)
	pickle.dump(regressor, open('model.pkl','wb'))
	model = pickle.load(open('model.pkl','rb'))
	print("Output 3:")
	a=model.predict([[int(day),int(time)]])
	
	a = (str(int(a//60))+":"+str(int(a%60))+":00")
	data = a
	cdjson['dataset3']['total_time']= data

	print("\n")
	dataset=dapi['dataset4']['data']
	x1 = [ xd['Day'] for xd in dataset ] 
	x2 = [ xd['Time Slots'] for xd in dataset ] 
	X = list(map(list,zip(x1,x2)))
	y = [ xy['Ttime'] for xy in dataset ]
	y1 = []
	for i in y:
	    j=i.split(":")
	    y1.append((int(j[0])*60)+int(j[1]))
	X_train, X_test, y1_train, y1_test = train_test_split(X, y1, test_size = 1/3, random_state = 0)
	regressor = LinearRegression()
	regressor.fit(X_train, y1_train)
	y1_pred = regressor.predict(X_test)
	pickle.dump(regressor, open('model.pkl','wb'))
	model = pickle.load(open('model.pkl','rb'))
	print("Output 4:")
	a=model.predict([[int(day),int(time)]])
	a = (str(int(a//60))+":"+str(int(a%60))+":00")
	
	data = a
	cdjson['dataset4']['total_time']= data

	return cdjson

if __name__ == '__main__':
    app.run(debug=True)