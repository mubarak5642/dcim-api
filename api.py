#!/usr/bin/env python3

from functools import wraps
from flask import request, Response, jsonify, Flask
import sqlite3
import pandas as pd
import base64
from datetime import datetime

app = Flask(__name__)

conn = sqlite3.connect('data.db')
db = pd.read_csv('PowerIQData.csv')
db.to_sql('power', conn, if_exists='replace', index=False)

db = pd.read_csv('sensorsData.csv')
db.to_sql('sensors', conn, if_exists='replace', index=False)

identity = {
    "data": {
        "type": "identity",
        "attributes": {
            "api_version" : "1.0",
            "make" : "Akamai Data Store",
            "model" : "Akamai Virtual Device"
        }
    }
}

def check(authorization_header):
    uname_pass = 'admin:sunbird'
    uname_pass_bytes = uname_pass.encode('ascii')
    base64_bytes = base64.b64encode(uname_pass_bytes)
    base64_uname_pass = base64_bytes.decode('ascii')

    encoded_uname_pass = authorization_header.split()[-1]
    if encoded_uname_pass == base64_uname_pass:
        return True

    return False

def get_error_response(error):
    return {
        "error": "{ERROR}".format(ERROR=error)
    }

def get_rack_sensors(piq_id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "SELECT * FROM sensors WHERE piq_id=?"
    result = cursor.execute(query, (piq_id,))
    row = result.fetchone()
    if not row:
        raise ValueError("Rack with ID {}, doesn't exists".format(piq_id))

    attributes = {}
    if row[3]:
        attributes["inlet_temperature_bottom"] = row[3]
    if row[4]:
        attributes["outlet_temperature_bottom"] = row[4]
    if row[5]:
        attributes["inlet_temperature_middle"] = row[5]
    if row[6]:
        attributes["outlet_temperature_middle"] = row[6]
    if row[7]:
        attributes["inlet_temperature_top"] = row[7]
    if row[8]:
        attributes["outlet_temperature_top"] = row[8]
    
    return [
        {
            "data": {
            "type": "rack_sensor_readings",
            "id": row[0],
            "attributes": attributes,
            "relationships": {
                "rack": {
                    "data": {
                        "id": row[1]
                    }
                }
            }
            }
        }
    ]

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@auth_required
def home():
    return "DCIM PowerIQ API"

@app.route('/identity')
@auth_required
def identity_requests():
    return jsonify(identity)
    
@app.route('/monitor/sensor_readings')
@auth_required  
def monitor_requests():
    server_id = request.args.get('filter[server_id]')
    if not server_id:
        return jsonify({'error': 'IP Address is required'}), 400

    servers = server_id.split(',')
    new_sensor_readings = []
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    for server in servers:
        query = "SELECT * FROM power WHERE ip_addr=?"
        result = cursor.execute(query, (server.strip(),))
        row = result.fetchone()
        
        if not row:
            new_sensor_readings.append(
                {'message': 'Ip address {} not found'.format(server)}
            )
            continue

        new_sensor_readings.append({
            'data': {
                'type': 'sensor_readings',
                'id': row[0],
                'attributes': {
                    'active_power_watts': row[3]
                },
                'relationships': {
                    'server': {
                        'data': {
                            'id': row[1]
                        }
                    }
                }
            }
        })
    
    return jsonify(new_sensor_readings)

@app.route('/monitor/rack_sensor_readings')
@auth_required
def monitor_temperature_requests():
    filter_parameter = 'filter[rack_id]'

    if filter_parameter not in request.args:
        return jsonify(get_error_response("Rack ID is required")), 400
    
    rack_id = request.args.get(filter_parameter)
    if not rack_id:
        return jsonify(get_error_response("Rack ID is required")), 400
    
    rack_id = rack_id.strip() 
    try:
        rack_id = int(rack_id)
    except ValueError:
        return jsonify(
            get_error_response("Rack ID {} must be integer".format(rack_id))
        ), 422
    
    try:
        return jsonify(get_rack_sensors(rack_id))
    except ValueError as e:
        return jsonify(get_error_response(str(e))), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
