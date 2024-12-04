import mysql.connector
import database as db
from utilities import log_setup,data_operator as dop
import traceback
from common_files import constants_file as cs
import mysql
import json

logger = log_setup.getlogger()

def get_alias_connection(alias):
    ''' Get DB connection based on Alias. Connection values are extracted from db_config.json'''
    try:
        with open(cs.db_config) as rd:
            db_config = json.load(rd)
            json_data = dop.get_value_from_json(db_config,alias)
            host = json_data['host']
            port = json_data['port']
            user = json_data['user']
            password = json_data['password']
            database = json_data['database']

            return get_db_connection(host,port,user,password,database)
    except:
        logger.error(traceback.format_exc())
        raise

def get_db_connection(host,port,user,password,database):
    ''' MYSQL db connection is established with the given host,port,username,password,db_schema'''
    try:
        connection = mysql.connector.connect(host=host,port=port,user=user,password=password,database=database)
        return connection
    except:
        logger.error(traceback.format_exc())
        raise



