# -*- coding: utf-8 -*-

from datetime import datetime

from eventviz import settings


class Parser(object):
    name = None
    time_fmt = ''
    base_indexes = [
        ('raw_log', True),
    ]
    extra_indexes = []
    regexes = []
    fieldnames = []

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return '<Parser:%s %s>' % (self.name, self.filename)

    def run(self):
        with open(self.filename) as inf:
            for line in inf:
                line = line.strip()
                if not line:
                    continue
                data = self.pre_parse(line)
                data = self.parse(data)
                data = self.normalize(data)
                data['raw_log'] = line
                yield data

    def pre_parse(self, line):
        return line

    def parse(self, line):
        match = None
        for regex in self.regexes:
            match = regex.match(line)
            if match is not None:
                return match.groupdict()
        if settings.DEBUG and (match is None):
            print'FAILED: %s' % line

    def normalize(self, data):
        data['time'] = datetime.strptime(data['time'], self.time_fmt)
        return data
