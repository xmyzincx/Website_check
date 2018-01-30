import json
from urlparse import urlparse
import urllib2
import time
import website_monitor

RES_FIELDS = [
    "url_check",
    "status_code_check",
    "status_code",
    "server_check",
    "content_type_check",
    "via_check",
    "must_contain_check",
    "should_contain_check",
    "may_contain_check",
    "redirect_url",
    "RTT"
]


resp_dict = {}
resp_dict.fromkeys(RES_FIELDS)

def analyze(website_reqrmnt):
    url = website_reqrmnt.get('url')
    url_parse = urlparse(url)

    # For the timebeing, this is just checking if URL contains scheme or not.
    # It can be made more sophisticated by using other packages such as Django
    # and validators packages. Otherwise specify correct URL in the config file.
    if not url_parse.scheme:
        url = 'http://' + url

    req = urllib2.Request(url)
    try:
        # Time when the request was sent
        send_time = time.time()
        # Sending request
        resp = urllib2.urlopen(req)
        # Time when the request was completed
        rcv_time = time.time()
        # Elapsed time in milliseconds upto 3 decimal points
        rtt_ms = round(rcv_time - send_time, 3)

        # Gathering all the necessary data
        html = unicode(resp.read(), errors='ignore')
        headers = resp.info()
        redirect_url = resp.geturl()

        resp_dict['RTT'] = rtt_ms

        # URL validation check
        resp_dict['url_check'] = True

        # Response status code check and the actual code if it differs
        http_code = resp.getcode()
        if website_reqrmnt.get('status_code') == http_code:
            resp_dict['status_code_check'] = True
        else:
            resp_dict['status_code_check'] = False
        resp_dict['status_code'] = http_code
        
        print "URL: {}, Status code: {}, RTT(ms): {}".format(url, http_code, rtt_ms)

        # Server name check
        if website_reqrmnt.get('server') == headers.get('server'):
            resp_dict['server_check'] = True
        else:
            resp_dict['server_check'] = False

        # Content type check
        if website_reqrmnt.get('content_type') == headers.get('content_type'):
            resp_dict['content_type_check'] = True
        else:
            resp_dict['content_type_check'] = False

        # Via and redirection check
        if website_reqrmnt.get('via') == headers.get('via'):
            resp_dict['via_check'] = True
        else:
            resp_dict['via_check'] = False
        resp_dict['redirect_url'] = redirect_url

        # String contain checks
        # This can be done in several ways, one using BeautifulSoup
        # and other is using normal python if condition for
        # string search e.g if substring in string.
        # Secondly, the most famous way is to use regex (Regular expression)
        # to find and match the string but it can introduce some complexities.
        # Here, I am using standard python method for simplicity.
        # Although I am pretty sure that this is not the efficient solution
        # and I think this can me implmented in more sophisticated ways.
        must_string_checks_list = []
        for string in website_reqrmnt.get('must_contain'):
            # Finding the very first occurance of the string.
            if string in html:
                must_string_checks_list.append(True)
            else:
                must_string_checks_list.append(False)
        resp_dict['must_contain_check'] = must_string_checks_list

        should_string_checks_list = []
        for string in website_reqrmnt.get('should_contain'):
            # Finding the very first occurance of the string.
            if string in html:
                should_string_checks_list.append(True)
            else:
                should_string_checks_list.append(False)
        resp_dict['should_contain_check'] = should_string_checks_list

        may_string_checks_list = []
        for string in website_reqrmnt.get('may_contain'):
            # Finding the very first occurance of the string.
            if string in html:
                may_string_checks_list.append(True)
            else:
                may_string_checks_list.append(False)
        resp_dict['may_contain_check'] = may_string_checks_list

    except urllib2.HTTPError as eHttp:
        print('Server unable to fulfill the request.')
        print('Error code: ', eHttp.code)
    except urllib2.URLError as eURL:
        print('Failed to reach server.')
        print('Reason: ', eURL.reason)

    if website_monitor.log:
        with open('results.json', 'a') as fp:
            json.dump(resp_dict, fp, sort_keys=True, indent=4)

    return resp_dict
