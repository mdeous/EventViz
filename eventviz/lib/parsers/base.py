# -*- coding: utf-8 -*-

from datetime import datetime

from eventviz import settings


class Parser(object):
    name = None
    time_fmt = ''
    indexes = [{'field': 'raw_event', 'unique': True}]
    fieldnames = []

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return '<Parser:%s %s>' % (self.name, self.filename)

    def add_db_index(self, field, unique=False):
        self.indexes.append({'field': field, 'unique': unique})

    def parse(self, line):
        raise NotImplementedError

    def normalize(self, data):
        data['time'] = datetime.strptime(data['time'], self.time_fmt)
        return data

    def run(self):
        with open(self.filename) as inf:
            for line in inf:
                line = line.strip()
                if not line:
                    continue
                data = self.parse(line)
                if data is None:
                    if settings.DEBUG:
                        print'FAILED: %s' % line
                    continue
                else:
                    if settings.DEBUG:
                        from pprint import pprint
                        pprint(data)
                data = self.normalize(data)
                data['raw_log'] = line
                yield data


class RegexParser(Parser):
    name = 'regex'
    regexes = []

    def parse(self, line):
        match = None
        for regex in self.regexes:
            match = regex.match(line)
            if match is not None:
                return match.groupdict()
