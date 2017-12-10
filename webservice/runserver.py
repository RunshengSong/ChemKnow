'''
Created on Jan 22, 2017

API for the webservice API

@author: Yiting & Runsheng
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import copy
import time, os, csv
from subprocess import Popen
from datetime import timedelta
from functools import update_wrapper

from flask_cors import CORS, cross_origin
from flask import Flask, request, redirect, jsonify, url_for, g, make_response, current_app

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from packages.chemical_name_identifier.annotateChem import *
from packages.txt2ChemReaction import *

CURRENT_MODEL = path.join(current_dir_path, "models", 'random_forest_0_0_1128')

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

def crossdomain(origin=None, methods=None, headers=None,
				max_age=21600, attach_to_all=True,
				automatic_options=True):

	if methods is not None:
		methods = ', '.join(sorted(x.upper() for x in methods))
	if headers is not None and not isinstance(headers, basestring):
		headers = ', '.join(x.upper() for x in headers)
	if not isinstance(origin, basestring):
		origin = ', '.join(origin)
	if isinstance(max_age, timedelta):
		max_age = max_age.total_seconds()

	def get_methods():
		if methods is not None:
			return methods

		options_resp = current_app.make_default_options_response()
		return options_resp.headers['allow']

	def decorator(f):
		def wrapped_function(*args, **kwargs):
			if automatic_options and request.method == 'OPTIONS':
				resp = current_app.make_default_options_response()
			else:
				resp = make_response(f(*args, **kwargs))
			if not attach_to_all and request.method != 'OPTIONS':
				return resp

			h = resp.headers

			h['Access-Control-Allow-Origin'] = origin
			h['Access-Control-Allow-Methods'] = get_methods()
			h['Access-Control-Max-Age'] = str(max_age)
			if headers is not None:
				h['Access-Control-Allow-Headers'] = headers
			return resp

		f.provide_automatic_options = False
		return update_wrapper(wrapped_function, f)
	return decorator

@app.route('/annotate', methods=['POST','GET'])
@crossdomain(origin='*')
# @cross_origin()
def run_ChemKnow():
	if request.method == 'POST':
		print "post in"
		text = request.form['text']
		targetChem = request.form['chem']
		hideChem = bool(request.form['hideChem'])

		print "Text: ",text
		print "Target Chemical: ", targetChem
		print "Hide Chemical Name? ", hideChem

		try:
			sentList, chemList = run_predict_on_text(text, targetChem, CURRENT_MODEL, hideChem)
			print chemList
			return jsonify({"results": {
				"sentList": sentList,
				"chemList": chemList
				}})
		except Exception,e:
			print str(e)
	elif request.method == "GET":
		print "get"
		text = request.args.get('text')
		targetChem = request.args.get('chem')
		hideChem = request.args.get('hideChem')
		print text

		print "111"
		if str(hideChem) == "1":
			hideChem = True
		else:
			hideChem = False
		print "Text: ",text
		print "Target Chemical: ", targetChem
		print "Hide Chemical Name? ", hideChem

		try:
			callPopen("python txt2ChemReaction.py " + "\""+ text +"\" " + targetChem + " " + str(hideChem))

			sentList, chemList = readResultFromCSV(os.path.join(current_dir_path, "theResult.csv"))



		except Exception,e:
			print str(e)

		else:
			# return jsonify({'results':  {
			#     'exposure': "111",
			#     'result': {"in":343}
			#     }})
			return jsonify({"results": {
				"sentList": sentList,
				"chemList": chemList
				}})
	else:
		return jsonify({'error':  {
				'err_msg': "request method is not supported"
				}})
		pass

def callPopen(command):
	print "Calling", command
	print current_dir_path
	try:
		e = Popen(
			command,
			# cwd="/home/yiting/Downloads/Vega-1.1.1-binaries/vega-cli beta 1_cmd",
			cwd = current_dir_path,
			shell=True
		)
		stdout, stderr = e.communicate()

	except IOError as (errno,strerror):
		print "I/O error({0}): {1}".format(errno, strerror)

def readResultFromCSV(csvFilePath):
	with open(csvFilePath, "rb") as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		sentList = []
		chemList = []
		rowCounter = 1
		for row in reader:
			if rowCounter == 1:
				for item in row:
					sentList.append(item)
			elif rowCounter == 2:
				for item in row:
					chemList.append(item)
			else:
				print rowCounter, row
				print "Wrong in reading csv"
			rowCounter += 1
	return sentList, chemList




if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port=5022, use_reloader=True, threaded=True)


