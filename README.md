# Website_check

This is simple script to check website status and their availibility

## Dependencies and limitations

This script was built using Python 2.7 and is not tested on later versions. Most of the dependencies are common and already available.

## Configuration
You can configure the script if following ways:
1- Define the number of thread workers by changing "thread_pool_size" parameter in "website_monitor.py". By-default is 2.
2- Define the polling interval by changing "checking_interval" parameter in "website_monitor.py". It is time in Milliseconds and default is 1000ms.
3- Number of hits you want to make to the websites by changing "number_of_hits" parameter in "website_monitor.py". Default is 0 which will continue testing the sites until the user stops the script.
4- Enable or disable logging output to the file. You can enable or diable by changing "log" parameter in "website_monitor.py". If enable, this will create a results.JSON file in the same directory with the following fields.
    "url_check" : Boolean,
    "status_code_check" : Boolean,
    "status_code" : HTTP response code,
    "server_check" : Boolean,
    "content_type_check" : Boolean,
    "via_check" : Boolean,
    "must_contain_check" : Array of type booleans,
    "should_contain_check" : Array of type booleans,
    "may_contain_check" : Array of type booleans,
    "redirect_url" : URL if redirected (Proxy),
    "RTT" : Round trip time in milliseconds

## Content requirements configuration file
You can set your requirements for a website in "config.json" present in the parent directory. Bare in mind that these are the requirements for the website response. Notable parameters in this config file:
    "url": URL or Website address,
    "status_code": HTTP response code,
    "server": Server name,
    "content_type": Content type of the response,
    "via": Check if the response is coming via proxy server,
    "must_contain": Array of strings you want to search,
    "should_contain": Array of strings you want to search,
    "may_contain": Array of strings you want to search

Example:

    "url": "http://www.google.com",
    "status_code": 200,
    "server": "gws",
    "content_type": "application/json",
    "via": "www-cache1.uusi.oulu.fi",
    "must_contain": ["Google", "Hello, world!", "Hello, world"],
    "should_contain": ["Hello, world!!", "Hello, world!", "Hello, world"],
    "may_contain": ["Hello, world!!", "Hello, world!", "Hello, world"]

## Running the script

You can run the script by following command:
python website_monitor.py

Note: You might need to add sudo if you are running on Linux machine.
