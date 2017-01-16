from flask import Flask, request, redirect, jsonify, url_for, g, make_response, current_app
import copy
import time, os, csv
from flask_cors import CORS, cross_origin
from annotateChem import annotateChemCS
from txt2ChemReaction import run_predict_on_text
from subprocess import Popen
from datetime import timedelta
from functools import update_wrapper


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)



current_dir_path = os.path.dirname(os.path.realpath(__file__))




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
def run_exposure():
	if request.method == 'POST':
		print "post in"
		text = request.form['text']
		targetChem = request.form['chem']
		hideChem = request.form['hideChem']
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

			# annotateChem_ins = annotateChem()
			# print "222"
			# apiResponse = annotateChem_ins.annotate(text)
			# if apiResponse == 1:
			# 	annotateResult = 1
			# elif apiResponse == 0:
			# 	annotateResult = 0
			# else:
			# 	print "Something is wrong in the class..."
			# this_sen, this_chems = run_predict_on_text(text, input_chemical_name=targetChem, find_chem_name=hideChem)        
			# print this_sen, this_chems
			# printName("RomaBoy")


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

		# # print type(request.form['qsar'])

		# qsar_result = {'qsar': request.form['qsar']}
		# fat_result = {'fat': request.form['fat']} 
		# print qsar_result['qsar']
		# print fat_result['fat']
		# """qsar_result and fat_result are the file path to the qsar_summary.json and sample_raw_output.csv on the server"""
		# try:
		#     expos_start_time = time.time()
		#     exposure_ins = Exposure()            

		#     expos_summary_json = exposure_ins.run(qsar_json_file_path=qsar_result['qsar'], 
		#         ft_csv_file_path=fat_result['fat'],
		#         place="LA",
		#         outputFilePath=os.path.join(exposure_ins.results_folder, "exposure_results.json"))

		#     print("--- Exposure Module finished in %s seconds ---" % (time.time() - expos_start_time))

		#     exposure_ins_results = os.path.join(exposure_ins.results_folder, "exposure_results.json")

		# except ModuleError:
		#     return jsonify()

		# else:
		#     return jsonify({'results':  {
		#         'exposure': exposure_ins_results,
		#         'result': expos_summary_json
		#         }})
		
		# return request.form['fat']
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


