# Pythonservice

Requirements

·        A service written in python or golang that queries 2 urls (https://httpstat.us/503 & https://httpstat.us/200)

·        The service will check the external urls (https://httpstat.us/503 & https://httpstat.us/200 ) are up (based on http status code 200) and response time in milliseconds

·        The service will run a simple http service that produces  metrics (on /metrics) and output a prometheus format when hitting the service /metrics url

·   Expected response format:

§  sample_external_url_up{url="https://httpstat.us/503 "}  = 0

§  sample_external_url_response_ms{url="https://httpstat.us/503 "}  = [value]

§  sample_external_url_up{url="https://httpstat.us/200 "}  = 1

§  sample_external_url_response_ms{url="https://httpstat.us/200 "}  = [value]



Deployement Procedure:

Clone the Repository 
--------------------

git clone https://github.com/shabarishetty46/Pythonservice.git

