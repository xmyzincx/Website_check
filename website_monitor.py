from __future__ import division
import json
import os
import sys
from multiprocessing.dummy import Pool as ThreadPool
import threading
from website_analyzer import analyze
import time


# Defining the field for data integrity.
# This is to keep the integrity between the config
# file and the fields used in the code
REQ_FIELDS = [
    "url",
    "status_code",
    "server",
    "content_type",
    "via",
    "must_contain",
    "should_contain",
    "may_contain"
]

# Options to do the tasks in multi threaded way.
# Some websites may take time to respond,
# therefore other threads will continue working on the other websites
thread_pool_size = 2

# Checking interval in milliseconds
checking_interval = 1000

# Number of times the whole test will run
number_of_hits = 1

# Path to config.json file
config_file_path = "config.json"

urls_dict = []

if __name__ == '__main__':

    # Loading the JSON file
    try:
        if os.path.getsize(config_file_path) > 0:
            json_file = json.load(open(config_file_path))
        else:
            print("File is empty!!")
            sys.exit()
    except OSError as e:
        print("Config file does not exist or is not accessible in the mentioned path.")
        sys.exit()
    except ValueError as e:
        print("Unable to decode config file. Or file is in improper format.")
        sys.exit()

    # This is again for integrity. If there is missing field,
    # this will create an empty field rather than null
    for website in json_file:
        # This is dict of requirements for a single URL
        url_reqrmnt = {x: website.get(x, '') for x in REQ_FIELDS}
        # Filling the list of URLs
        urls_dict.append(url_reqrmnt)
        #print(url_reqrmnt)

    for i in range(0, number_of_hits):

        threads_pool = ThreadPool(thread_pool_size)

        threads_pool.map(analyze, urls_dict)

        threads_pool.close
        threads_pool.join

        time.sleep(checking_interval/1000)

        
