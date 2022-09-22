# DCIM PowerIQ API

## API routes

#### GET /

Returns 'DCIM PowerIQ API'

#### GET /identity

Identity requests will be used by PIQ to identify and discover the ADS and validate the facility item's credentials as configured in dcTrack/PIQ.

#### GET /monitor/sensor_readings?filter[server_id]=<comma_separated_list_of_ips>

Monitor requests will retrieve sensor readings for a set of server identifiers (i.e., IP addresses) passed in the request URL.

#### GET /monitor/rack_sensor_readings?filter[rack_id]=<RACK ID from PowerIQ>

##### Example-1: ```/monitor/rack_sensor_readings?filter[rack_id]=100```
Response contains complete sensor readings

##### Example-2: ```/monitor/rack_sensor_readings?filter[rack_id]=101```
Response contains incomplete sensor readings - doesn't have middle sensors data

##### Example-3: ```/monitor/rack_sensor_readings?filter[rack_id]=105```
Response contains incomplete sensor readings - doesn't have any sensors data

Monitor requests will retrieve rack sensor readings passed in the request URL for the given PIQ rack ID.
  
##### Note: Modify ```sensorsData.CSV``` for testing for realtime PIQ and dcTrack's ITEM ids.

#### Run the application using following commands

```
docker build . -t dcim-api
docker run -p 443:443 -t -i dcim-api:latest

```
check the response with https://localhost/
