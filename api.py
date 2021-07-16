#!/usr/bin/env python3
from functools import wraps
from flask import request, Response, jsonify, Flask
import sqlite3
import pandas as pd
import base64

app = Flask(__name__)

conn = sqlite3.connect('data.db')
db = pd.read_csv('PowerIQData.csv')
db.to_sql('power', conn, if_exists='replace', index=False)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
