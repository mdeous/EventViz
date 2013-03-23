# -*- coding: utf-8 -*-

from datetime import datetime

from eventviz import settings


class Parser(object):
    name = None
    time_fmt = ''
    base_indexes = [
        ('time', False),
        ('raw_log', True)
    ]
    extra_indexes = []
    regexes = []
    fieldnames = []

    def __init__(self, filename):
        self.filename = filename

    @property
    def items(self):
        with open(self.filename) as inf:
            for line in inf:
                line = line.strip()
                if not line:
                    continue
                line = self.pre_parse(line)
                for regex in self.regexes:
                    match = regex.match(line)
                    if match is not None:
                        data = self.normalize(match.groupdict())
                        data['time'] = datetime.strptime(data['time'], self.time_fmt)
                        data['raw_log'] = line
                        yield data
                        break
                if settings.DEBUG and (match is None):
                    print'FAILED: %s' % line

    def pre_parse(self, line):
        return line

    def normalize(self, data):
        return data
