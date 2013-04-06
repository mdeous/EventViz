# -*- coding: utf-8 -*-

from eventviz.lib.parsers.parser import Parser
from eventviz.lib.parsers.apache import ApacheAccessParser


def get_parser_by_name(name):
    for parser in Parser.__subclasses__():
        if parser.name == name:
            return parser
    return None


def get_parser_names():
    return [parser.name for parser in Parser.__subclasses__()]
