# -*- coding: utf-8 -*-

import re

from eventviz.lib.parsers.parser import Parser

# LogFormat "%h %l %u %t \"%m /%v%U%q %H\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %D %{SESSIONID}C" custom_combined
# TODO LogFormat "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
# TODO LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined
# TODO LogFormat "%h %l %u %t \"%r\" %>s %b" common
# TODO LogFormat "%{Referer}i -> %U" referer
# TODO LogFormat "%{User-agent}i" agent


class ApacheAccessParser(Parser):
    name = 'apache_access'
    time_fmt = '%d/%b/%Y:%H:%M:%S'
    regexes = [
        re.compile(
            r'^'
            r'(?P<source_ip>(?:\d{1,3}\.){3}\d{1,3}) '  # source ip
            r'(?P<remote_logname>[^ ]+) '  # remote logname
            r'(?P<remote_user>[^ ]+) '  # remote user
            r'\[(?P<time>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] '  # time
            r'"(?P<method>[^ ]+) '  # method
            r'(?P<querystring>.*?) '  # query
            r'(?P<protocol>[^"]+)" '  # protocol
            r'(?P<status>\d{3}) '  # status code
            r'(?P<resp_size>\d+|-)(?: '  # response size
            r'"(?P<referrer>.*)" '  # referrer (optional)
            r'"(?P<user_agent>.*?)" '  # user-agent (optional)
            r'(?P<process_time>\d+) '  # process_time (optional)
            r'(?P<session_id>.+))?'  # session id (optional)
            r'$'
        ),
    ]
    fixed_fields = [
        'source_ip', 'remote_logname', 'remote_user', 'time', 'method', 'querystring', 'protocol', 'status', 'resp_size'
    ]

    def normalize(self, data):
        data['time'] = data['time'][:-6]
        return data
