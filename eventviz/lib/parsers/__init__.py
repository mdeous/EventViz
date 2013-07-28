# -*- coding: utf-8 -*-

from itertools import chain

from eventviz.lib.parsers.base import Parser, RegexParser
from eventviz.lib.parsers.apache import ApacheAccessParser

BASE_PARSER_CLASSES = (
    Parser,
    RegexParser
)
IGNORED_PARSER_NAMES = (
    'regex',
)
PARSER_SUBCLASSES = list(chain(*[p.__subclasses__() for p in BASE_PARSER_CLASSES]))


def get_parser_by_name(name):
    for parser in PARSER_SUBCLASSES:
        if parser.name in IGNORED_PARSER_NAMES:
            continue
        if parser.name == name:
            return parser
    return None


def get_parser_names():
    return [p.name for p in PARSER_SUBCLASSES if p.name not in IGNORED_PARSER_NAMES]
