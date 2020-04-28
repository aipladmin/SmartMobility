from flask import Flask,request,jsonify
import pandas as pd
import json
app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(debug=True)