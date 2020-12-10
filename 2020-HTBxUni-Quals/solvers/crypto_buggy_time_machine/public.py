import os
from datetime import datetime
from flask import Flask, render_template
from flask import request
import random
from math import gcd
import json
from secret import flag, hops, msg

class TimeMachineCore:
	
	n = ...
	m = ...
	c = ...
		

	def __init__(self, seed):
		self.year = seed 

	def next(self):
		self.year = (self.year * self.m + self.c) % self.n
		return self.year

app = Flask(__name__)
a = datetime.now()
seed = int(a.strftime('%Y%m%d')) <<1337 % random.getrandbits(128)
gen = TimeMachineCore(seed)


@app.route('/next_year')
def next_year():
	return json.dumps({'year':str(gen.next())})

@app.route('/predict_year', methods = ['POST'])
def predict_year():
	
	prediction = request.json['year']
	try:

		if prediction ==gen.next():
			return json.dumps({'msg': msg})
		else:
			return json.dumps({'fail': 'wrong year'})

	except:

		return json.dumps({'error': 'year not found in keys.'})

@app.route('/travelTo2020', methods = ['POST'])
def travelTo2020():
	seed = request.json['seed']
	gen = TimeMachineCore(seed)
	for i in range(hops): state = gen.next()
	if state == 2020:
		return json.dumps({'flag': flag})

@app.route('/')
def home():
	return render_template('index.html')
if __name__ == '__main__':
	app.run(debug=True)



