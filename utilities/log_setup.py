'''
Summary 
In this code:

- We define a custom function check_file_size(log_file) to check if the log file's size exceeds 5 MB.
- We check the file size before creating the rotating file handler. 
    If the size exceeds 5 MB, we truncate the file by opening it in write mode ('w') and immediately closing it (close()).
- We then create the RotatingFileHandler with a max size of 10 MB and a backup count of 1.
- The rest of the code sets up logging and demonstrates example usage.
- This setup ensures that existing data in the log file will be deleted if the file size exceeds 5 MB before logging new data. 
    Adjust the file size limit and other parameters as needed.
'''

import logging
import os
from logging.handlers import RotatingFileHandler

if not os.path.exists('/logs'):
    os.mkdir('/logs')



# Check if the file size is greater than 5 mb

def check_file_size(logfile):
    '''Check if the file size is greater than 5 mb'''
    return os.path.exists(logfile) and os.stat(logfile).st_size > 5 * 1024 * 1024

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_path = 'log_file.log'
log_file = os.path.join('logs', log_path)


# Check if file size exceeds 5 MB before creating rotating handler
if check_file_size(log_file):
    open(log_file,'w').close()

# Create a rotating file handler with max size of 10 MB
'''Using a logging handler called RotatingFilehandler can help you rotate your log files. 
Rotating log files is when you save log messages to a file, and when that file hits a predetermined size, 
a new file is created. The handler files. 
RotatingFileHander will rotate log files based on a user-configured maximum size'''

rotating_handler = RotatingFileHandler(log_file,mode='a',maxBytes=10*1024*1024,backupCount=1)
rotating_handler.setFormatter(log_formatter)


# Get the root logger and add the rotating handler
def getlogger():
    logger = logging.getLogger()
    logger.addHandler(rotating_handler)
    logger.setLevel(logging.DEBUG) # Set the root logger's level to DEBUG

    return logger