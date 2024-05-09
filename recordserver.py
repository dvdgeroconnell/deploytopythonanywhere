# record_server.py
#
# Main python file and REST server for WSAA Final Project.
# See README for instrunctions on use and curl commands to test.
#
# David O'Connell

from flask import Flask, jsonify, url_for, request, redirect, abort, make_response
from flask_cors import CORS, cross_origin
from recordDAO import recordDAO
import sys

# Had to enable CORS headers in flask. This site helped, as well as flask documentation.
# https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
# Probably not needed in PythonAnywhere based version, but they are working there.

app = Flask(__name__, static_url_path='', static_folder='staticpages')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# This is global, as declarred outside of any function
local_env = False

#------------------------------------------------------------------------
# Build response to incoming OPTIONS request

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

#------------------------------------------------------------------------
# Index

@app.route('/')
@cross_origin()
def index():
    return {"response":"hello"}

#------------------------------------------------------------------------
# Get all records
# Local: curl -X GET http://127.0.0.1:5000/records

@app.route('/records', methods=["GET", "OPTIONS"])
@cross_origin()

def get_all():
    if request.method == "OPTIONS": # CORS preflight
        print("get_all OPTIONS")
        return _build_cors_preflight_response()
    # Get the response object
    #return jsonify(recordDAO.get_all_records())
    response = jsonify(recordDAO.get_all_records())
    #response.headers.add("Access-Control-Allow-Origin", "*")
    return response

#------------------------------------------------------------------------
# Get record by ID
# Local: curl -X GET http://127.0.0.1:5000/records/2

@app.route('/records/<int:id>', methods=["GET", "OPTIONS"])
@cross_origin()

def find_by_id(id):
    if request.method == "OPTIONS": # CORS preflight
        print("find_by_id OPTIONS")
        return _build_cors_preflight_response()
    # Get the response object
    #return jsonify(recordDAO.find_record_by_id(id))
    response = jsonify(recordDAO.find_record_by_id(id))
    #response.headers.add("Access-Control-Allow-Origin", "*")
    return response

#------------------------------------------------------------------------
# Create a record
#curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"Closer\", 
# \"artist\":\"Joy Division\", \"year\":1981, \"genre\":\"post punk\"}" 
# Local: http://127.0.0.1:5000/records

@app.route('/records', methods=["POST", "OPTIONS"])
@cross_origin()

def create():
    # Read the JSON from the body of the incoming request
    record = {}
    record_string = request.json
    
    if request.method == "OPTIONS": # CORS preflight
        print("create OPTIONS")
        return _build_cors_preflight_response()

    # build the record to create - check each field is present
    if "title" not in record_string:
        abort(400)
    record["title"] = record_string["title"]

    if "artist" not in record_string:
        abort(400)
    record["artist"] = record_string["artist"]

    if "year" not in record_string:
        abort(400)
    record["year"] = record_string["year"]

    if "genre" not in record_string:
        abort(400)
    record["genre"] = record_string["genre"]

    # Create the record, get the response object
    print("Creating", record)
    #return jsonify(recordDAO.create_record(record))
    response = jsonify(recordDAO.create_record(record))
    #response.headers.add("Access-Control-Allow-Origin", "*")
    return response

#------------------------------------------------------------------------
# Update a record
#curl -X PUT -H "Content-Type: application/json" -d "{\"title\":\"Further\"}" 
#http://127.0.0.1:5000/records/5

@app.route('/records/<int:id>', methods=["PUT", "OPTIONS"])
@cross_origin()

def update(id):
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()

    # Read the JSON from the body of the incoming request
    record = {}
    record_string = request.json

    # Build the update
    if "title" in record_string:
        record["title"] = record_string["title"]
    if "artist" in record_string:
        record["artist"] = record_string["artist"]
    if "year" in record_string:
        record["year"] = record_string["year"]
    if "genre" in record_string:
        record["genre"] = record_string["genre"]

    # Update the record, get the response object
    print("Updating record", id, "to", record)
    #return jsonify(recordDAO.update_record(id, record))
    response = jsonify(recordDAO.update_record(id, record))
    #response.headers.add("Access-Control-Allow-Origin", "*")
    return response

#------------------------------------------------------------------------
# Delete a record
# curl -X DELETE http://127.0.0.1:5000/records/5

@app.route('/records/<int:id>', methods=["DELETE", "OPTIONS"])
@cross_origin()

def delete(id):
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    # Delete the record, get the response object
    if recordDAO.delete_record(id):
        #return jsonify(recordDAO.delete_record(id))
        #return jsonify({"done":True})
        response = jsonify({"done":True})
        #response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
#------------------------------------------------------------------------

if (len(sys.argv)) > 1:
    local = sys.argv[1]
    if local == "local":
        local_env = True
        print("Running local app server instance")

# For anything other than "local"...
if not local_env:
    print("Running PythonAnywhere app server instance")

if __name__ == "__main__":
    app.run(debug=True)