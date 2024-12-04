'''
All data operator functions includes, 
* set_value_to_json -     Set the value of a specific key in a JSON object. 
* extract_file_json -   Extract JSON content from a file.
* get_value_from_json - Get value of JSON key for a JSON request.
* get_jsonpath - Get JSON path of key from a request. 
* get_value_by_jsonpath - Get Value of key based on JSON path.
* is_value_present_json - Check if values is present in the JSON response. Returns boolean
* random_name_generator - Generates random name based on User preference length
* generate_random_integer - Generates random number based on User preference range
* get_system_date - Gets system current date in the format YYYY-MM-DD
* get_past_date - Gets past date by user specificed difference in the format YYYY-MM-DD
* get_future_date - Gets future date by user specificed addition in the format YYYY-MM-DD




'''

import json
from utilities import log_setup
import traceback
import string
import random
import datetime 

logger = log_setup.getlogger()

def set_value_to_json(json_data,key,value):
    '''
    Set the value of a specific key in a JSON object. 
    Using Recursive search and update the JSON object.

    '''
    # Helper function to recursively search and update the JSON object
    def set_json(json_data,key,value):
        if isinstance(json_data,dict):
            for k,v in json_data.items():
                if k==key:
                    json_data[key]=value
                else:
                    set_json(v,key,value)
        if isinstance(json_data,list):
            for item in json_data:
                set_json(item,key,value)
    set_json(json_data,key,value)

    return json_data


def extract_file_json(file_path):
    '''Extract JSON content from a file. Mostly used to build input Payload of an API'''
    try:
        with open(file_path,'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logger.error(f"Error Occured: File not found at path: {file_path}")
        logger.error("Error Occured: "+ traceback.format_exc())
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file: {e}")
        return None
    

def get_value_from_json(jsondata,key):
    ''' Get value of JSON key. Used to Extract response values'''
    if isinstance(jsondata,dict):
        for k,v in jsondata.items():
            if k==key:
                return v
            else:
                if isinstance(v,dict) or isinstance(v,list):
                    result = get_value_from_json(v,key)
                    if result is not None:
                        return result

    if isinstance(jsondata,list):
        for item in jsondata:
            result = get_value_from_json(item,key)
            if result is not None:
                return result

def get_jsonpath(json_data, target_key, current_path="", paths=[]):
    '''Get JSON path of key from a request. '''
    if isinstance(json_data,dict):
        for k,v in json_data.items():
            if k==target_key:
                paths.append(f"{current_path}.{k}")
            elif isinstance(v,dict) or isinstance(v,list):
                get_jsonpath(v, target_key, f"{current_path}.{k}", paths)
    
    elif isinstance(json_data,list):
        for i,item in enumerate(json_data):
            get_jsonpath(item,target_key, f"{current_path}.{[i]}", paths)

    return paths



def get_value_by_jsonpath(json_data,json_path):
    ''' Get Value of key based on JSON path.'''
    ''' # Split the JSON path into its components
        # Traverse each component of the JSON path
        # If the component is a digit, treat the current object as a list and get the corresponding index
        # If the component is a key, treat the current object as a dictionary and get the corresponding value
    '''
    try:
        path_components = json_path.split('.')
        current_obj = json_data

        for component in path_components:
            if component.isdigit():
                current_obj = current_obj[int(component)]
            else:
                current_obj = current_obj.get(component)

            if current_obj is None:
                return None
        return current_obj

    except:
        logger.error(traceback.format_exc())


def is_value_present_json(json_data, value):
    ''' Check if values is present in the JSON response. Returns boolean'''
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if v == value:
                return True
            elif isinstance(v, dict) or isinstance(v, list):
                if is_value_present_json(v, value):
                    return True
    elif isinstance(json_data, list):
        for item in json_data:
            if is_value_present_json(item, value):
                return True
    return False

def random_name_generator(length):
    '''Generates random name based on User preference length.'''
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length)).lower()

def generate_random_integer(min_value, max_value):
    '''Generates random number based on User preference range.'''

    return random.randint(min_value, max_value)

def get_system_date():
    '''Gets system current date in the format YYYY-MM-DD'''
    date_str = datetime.date.today().strftime('%Y-%m-%d')
    return date_str

def get_past_date(days):
    '''Gets past date by user specificed difference in the format YYYY-MM-DD'''
    delta = datetime.date.today() - datetime.timedelta(days=days)
    return delta.strftime('%Y-%m-%d')

def get_future_date(days):
    '''Gets future date by user specificed addition in the format YYYY-MM-DD'''
    delta = datetime.date.today() + datetime.timedelta(days=days)
    return delta.strftime('%Y-%m-%d')


