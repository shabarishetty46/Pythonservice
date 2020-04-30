import requests
# urllib3 package to fix the ssl verify error
import urllib3
urllib3.disable_warnings()

url=['https://httpstat.us/503','https://httpstat.us/200']

for i in url:
    # response 
    response=requests.get(i, verify=False)
    # store the statuscodes
    status=response.status_code
    # store the response time in milliseconds
    time=str(round(response.elapsed.total_seconds(),2))
    if status==200:
        print('sample_external_url_up{url=' '"' + str(i) + '"' '}=1')
    else:
        print('sample_external_url_up{url=' '"' + str(i) + '"' '}=0')
    print('sample_external_url_response_ms{url=' '"' + str(i) + '"' '}=%s'%(time))

