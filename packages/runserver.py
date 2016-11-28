from flask import Flask, request, redirect, jsonify, url_for, g, make_response, current_app
import copy
import time, os
from flask_cors import CORS, cross_origin
from annotateChem import annotateChem


app = Flask(__name__)
CORS(app)





@app.route('/annotate', methods=['POST','GET'])
@cross_origin()
def run_exposure():
	print "Start running Exposure Module"
	if request.method == 'POST':
		print "post in"
		text = request.form['text']
		print text

		try:
			print "111"
			annotateChem_ins = annotateChem()
			print "222"
			apiResponse = annotateChem_ins.annotate(text)
			if apiResponse == 1:
				annotateResult = 1
			elif apiResponse == 0:
				annotateResult = 0
			else:
				print "Something is wrong in the class..."

		except Exception,e:
			print str(e)

		else:
			# return jsonify({'results':  {
			#     'exposure': "111",
			#     'result': {"in":343}
			#     }})
			return jsonify({"results": {
				"annotate": annotateResult,
				"text": text
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
		print text

		try:
			print "111"
			annotateChem_ins = annotateChem()
			print "222"
			apiResponse = annotateChem_ins.search(text)
			if apiResponse == True:
				annotateResult = 1
			else:
				annotateResult = 0

		except Exception,e:
			print str(e)

		else:
			# return jsonify({'results':  {
			#     'exposure': "111",
			#     'result': {"in":343}
			#     }})
			return jsonify({"results": {
				"annotate": annotateResult,
				"text": text
				}})
	else:
		return jsonify({'error':  {
				'err_msg': "request method is not supported"
				}})
		pass




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
			h['Access-Control-Allow-Credentials'] = 'true'
			h['Access-Control-Allow-Headers'] = \
				"Origin, X-Requested-With, Content-Type, Accept, Authorization"
			if headers is not None:
				h['Access-Control-Allow-Headers'] = headers
			return resp

		f.provide_automatic_options = False
		return update_wrapper(wrapped_function, f)
	return decorator




if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', use_reloader=True, threaded=True)


