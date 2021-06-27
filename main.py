import flask, os, json, datetime
from flask import render_template, request, redirect, url_for, jsonify, make_response
from datetime import datetime

''' 
json format

settings.json
{
"work_time" : array[]
"break_time" : array[]
"raw_time" : array[]
"sessions" : int
"current_sessino" : int
"start_time" : string
}

logs.json
}
ID : {
	settings.json
	 }
}
'''

app = flask.Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def root():
	if (request.method == "POST"):
		settings = request.form
		work_time = convert_time(settings["work_time"])
		break_time = convert_time(settings["break_time"])

		data_file = load_json("settings.json")
		data_file["work_time"] = work_time	
		data_file["break_time"] = break_time	
		data_file["sessions"] = int(settings["sessions"])
		data_file["current_session"] = 1
		data_file["name"] = settings["name"]
		data_file["raw_time"] = [settings["work_time"], settings["break_time"]]
		data_file["start_time"] = datetime.now().strftime("%I:%M %p, %d-%m-%Y")
		data_file["tasks"] = []
		data_file["completed"] = []

		write_json(data_file, "settings.json")
		
		return redirect(url_for("todo"))

	return render_template("setup.html", settings = load_json("settings.json"))


@app.route('/work', methods = ["POST", "GET"])	
def work():
	return render_template("work.html", settings = load_json("settings.json"))

@app.route('/rest')
def rest():
	return render_template("rest.html", settings = load_json("settings.json"))

@app.route('/todo', methods = ["POST", "GET"])
def todo():
	return render_template("todo.html", settings = load_json("settings.json"))

@app.route("/sessions")
def sessions():
	return render_template("sessions.html", logs = load_json("logs.json"))

@app.route("/complete")
def complete():
	return render_template("complete.html", settings = load_json("settings.json"))

@app.route("/getdata", methods = ["POST"])
def getdata():
	'''
	Sends current timer settings to dynamically render html page
	'''
	data = load_json("settings.json")
	response = make_response(jsonify(data), 200)
	return response

@app.route("/add", methods = ["POST"])
def add():
	'''
	Adds task to todolist
	'''
	req = request.get_json()
	data = load_json("settings.json")
	data["tasks"].append(req["task"])
	write_json(data, "settings.json")
	response = make_response(jsonify(data), 200)
	return response


@app.route("/delete", methods = ["POST"])
def delete():
	'''
	Remove task from todolist
	'''
	req = request.get_json()
	data = load_json("settings.json")
	if (req["page"]):
		data["completed"].append(data["tasks"][req["task_id"]])

	data["tasks"].pop(req["task_id"])
	write_json(data, "settings.json")
	response = make_response(jsonify(data), 200)
	return response

@app.route("/workend", methods = ["POST"])
def workend():
	'''
	Starts/ends work session
	'''
	data = load_json("settings.json")
	if (data["current_session"] == data["sessions"]): # all sessions have been completed
		log_session()
		response = make_response(jsonify(data), 204)
	else:
		response = make_response(jsonify(data), 200)
	data["current_session"] += 1
	write_json(data, "settings.json")
	return response

@app.errorhandler(404)
def not_found(e):
	return render_template("404.html")

# Helper functions
def load_json(ff):
	if (os.path.exists(ff)):
		with open(ff) as datafile:
			saved_data = json.load(datafile)
	else:
		saved_data = {}

	return saved_data

def write_json(upd_data, target_file):
	with open(target_file, "w") as datafile:
		json.dump(upd_data, datafile, indent = 4)

def log_session():
	timestamp = datetime.now().strftime("%I:%M %p, %d-%m-%Y")
	log_file = load_json("logs.json")
	session_number = len(log_file.keys()) + 1
	log_file[session_number] = load_json("settings.json")
	log_file[session_number]["end_time"] = timestamp
	write_json(log_file, "logs.json")
 
def convert_time(tt):
	tt = int(tt)
	hours = tt // 60
	minutes = tt - (hours * 60)
	seconds = tt * 60
	return [hours, minutes, seconds]


app.run(host="0.0.0.0", port = 8080, debug = True)