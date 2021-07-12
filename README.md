# DCIM PowerIQ API

## API routes

#### GET /

Returns 'DCIM PowerIQ API'

#### GET /identity

Identity requests will be used by PIQ to identify and discover the ADS and validate the facility item's credentials as configured in dcTrack/PIQ.

#### GET /monitor/sensor_readings?filter[server_id]=<comma_separated_list_of_ips>

Monitor requests will retrieve sensor readings for a set of server identifiers (i.e., IP addresses) passed in the request URL.

Run the application using following commands

```
docker build . -t dcim-api
docker run -p 443:443 -t -i dcim-api:latest

```
check the response with localhost:443
