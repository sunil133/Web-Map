import arcpy
import json
import os
from arcpy import env
import urllib
import http.client  as httplib
import urllib.request
import requests
from requests.auth import HTTPBasicAuth
from arcgis.gis import GIS

print ("Test")
refer_url = 'https://dv-gis.dev.southernwater.co.uk/portal/'
token=''


user_name =  'portaladmin'
pswd =   'SouthernWater2022Dev' 
try:
    print ('Started')
    url = 'https://dv-gis.dev.southernwater.co.uk/portal/sharing/rest/generateToken?'
    payload = {
        "username":(None,user_name),
        "password":(None,pswd),
##        "client" :(None,'ip'),
##        "ip":(None,'10.184.7.50'),
        "referer":(None,refer_url),
        "expiration":(None,100),
        "f":(None,'json'),
        }
    print(1)
    response = requests.post(url,files=payload)
    response.raise_for_status()
    data = response.json()
    if 'token' in data:
        token=data['token']
        auth_token = token
        print(token)
    elif 'error' in data:
        
        print(data['error']['message'],4)
        for details in data['error']['details']:
            print(details)

            
    print("Start Post")
    
    
    with open(r'E:\Cyient\Users\Sunil\cweb_json\DD_YY_Format\DEV_LS_171123.json') as f:
       test_file = json.load(f)
       test_file = json.dumps(test_file)
      ## print(test_file)

    test_url = "https://dv-gis.dev.southernwater.co.uk/portal/sharing/rest/content/users/portaladmin///items/eb0ef5e7cc814ab995ca88cce19d8752/update"
    
    params = {'token': auth_token,"text":test_file,"f":"json"}#, 'format': 'json'}
    
    test_response = requests.post(test_url, data=params)    #, files = {"text":test_file })
    print("response")
    test_response.raise_for_status()
    print(test_response.text)
    
##    print(test_response)
##    print(test_response.json())
    if test_response.ok:
        print("Upload completed successfully!")
        print(test_response.text)
    else:
        print("Something went wrong!")

except Exception as inst:
    print(inst)

print ('Completed')
    
