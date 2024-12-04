import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
from utilities import log_setup
import traceback
import pytest
from utilities import data_operator as dop
logger = log_setup.getlogger()
'''
- Create a custom Retry object with dynamic retry logic (max_retries, HTTP status code to retry, HTTPs methods ot retry)
- Create a custom HTTPAdapter with the dynamic retry strategy
- Create a session and mount the custom adapter (Mount is used to customize and control the behaviour of HTTP response)
- Now use this session to make requests
- Check the response
'''

def get_session():
    '''
    Sessions in Python Requests provide a convenient and efficient way to manage state, authentication, and common parameters across multiple HTTP requests. 
    '''
    retry = Retry(total=3, status_forcelist=[500,502,503],allowed_methods=["GET","POST","PUT","DELETE"])
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount('http://',adapter)
    session.mount('https://',adapter)
    
    return session

def run_api(url, payload, headers, request_type=""):
    ''' Method is called to execute API request (GET,PUT,POST,DELETE) and extract response details'''

    try:
        if isinstance(payload, dict):
                payload = json.dumps(payload)
        
        logger.debug("url: "+url)
        logger.debug("request_payload: "+payload)
        logger.debug("request_headers: "+headers)
        logger.debug("request_type: "+request_type)

        session = get_session()
        response = ""

        if request_type.lower()=="get":
            response = session.get(url=url, headers=headers, data=payload, verify=False)

        if request_type.lower()=="post":
            response = session.post(url=url, headers=headers, data=payload, verify=False)

        if request_type.lower()=="put":
            response = session.put(url=url, headers=headers, data=payload, verify=False)

        if request_type.lower()=="delete":
            response = session.delete(url=url, headers=headers, data=payload, verify=False)
        
        if request_type.lower()=="patch":
            response = session.patch(url=url, headers=headers, data=payload, verify=False)

        response_headers = response.headers
        status_code = response.status_code
        response_body = ""
        if isinstance(response,dict):
            response_body = response.json()
            logger.debug("response_body: "+response_body)
        if isinstance(response,str):
            response_body = response.text
            logger.debug("response_body: "+response_body)
        if response == "":
            response_body = ""

        logger.debug("status_code: "+str(status_code))
        return status_code, response_body, response_headers

    except:
        logger.error("Error occured:" +traceback.format_exc())



def create_payload(payload, request_key_value):
    '''
    Method to replace the incoming Dictonary values to JSON request.
    payload - json - Dict
    request_key_value - replaceable Key-Value pairs
    '''

    if isinstance(payload, dict):
        for key, value in payload.items():
            if isinstance(value, dict) or isinstance(value, list):
                create_payload(value, request_key_value)
            elif key in request_key_value:
                payload[key] = request_key_value[key]
    elif isinstance(payload, list):
        for i in range(len(payload)):
            if isinstance(payload[i], dict) or isinstance(payload[i], list):
                create_payload(payload[i], request_key_value)
    return payload

