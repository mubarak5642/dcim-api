# DCIM PowerIQ API

## API routes

#### GET /

Returns 'DCIM PowerIQ API'

#### GET /identity

Identity requests will be used by PIQ to identify and discover the ADS and validate the facility item's credentials as configured in dcTrack/PIQ.

#### GET /identity/power_panel

Identity requests will be used by PIQ to identify and discover the ADS and validate the facility item credentials as configured in dcTrack/PIQ. This request will only be issued if right conditions on custom field 1 and 2 are met. Otherwise, the previous identity request will be used.

#### GET /monitor/sensor_readings?filter[server_id]=<comma_separated_list_of_ips>

Monitor requests will retrieve sensor readings for a set of server identifiers (i.e., IP addresses) passed in the request URL.

##### Note: Example IPs are in ```PowerIQData.CSV``` for testing.

##### Example-1: ```/monitor/sensor_readings?filter[server_id]=192.168.1.10,192.168.1.11```
Response contains complete sensor readings for IPs 192.168.1.10 and 192.168.1.11

#### GET /monitor/sensor_readings?filter[power_panel_id]=<Power Panel ID AKA Datacenter ID>

Monitor requests will be used by PIQ to perform data collection of power readings following initial discovery. This request will retrieve sensor readings for a power panel id passed in the request URL

##### Note: Example Power Panel IDs are in ```coloData.CSV``` for testing.

##### Example-1: ```/monitor/sensor_readings?filter[power_panel_id]=B-W-10AOCA```
Response contains complete sensor readings for power panel id B-W-10AOCA

#### GET /monitor/rack_sensor_readings?filter[rack_id]=<RACK ID from PowerIQ>

Monitor requests will retrieve rack sensor readings passed in the request URL for the given PIQ rack ID.

##### Example-1: ```/monitor/rack_sensor_readings?filter[rack_id]=100```
Response contains complete sensor readings

##### Example-2: ```/monitor/rack_sensor_readings?filter[rack_id]=101```
Response contains incomplete sensor readings - doesn't have middle sensors data

##### Example-3: ```/monitor/rack_sensor_readings?filter[rack_id]=105```
Response contains incomplete sensor readings - doesn't have any sensors data

##### Note: Modify ```sensorsData.CSV``` for testing for realtime PIQ and dcTrack's ITEM ids.

#### Run the application using following commands

```
docker build . -t dcim-api
docker run -p 443:443 -t -i dcim-api:latest

```
check the response with https://localhost/
