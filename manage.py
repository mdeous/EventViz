#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from flask.ext.script import Manager, Command, Option

from eventviz.app import app
from eventviz.db import insert_item, connection, get_database_names
from eventviz.lib.parsers import get_parser_by_name, get_parser_names


class LoadData(Command):
    """
    Parses a file and load its data in the database.
    """
    option_list = (
        Option('-f', '--filename', dest='filename', required=True),
        Option('-p', '--parser', dest='parser_name', required=True),
        Option('-P', '--project', dest='project_name', required=True)
    )

    def run(self, filename, parser_name, project_name):
        parser_cls = get_parser_by_name(parser_name)
        if parser_cls is None:
            print "Unknown parser: %s" % parser_name
            return
        if not os.path.exists(filename):
            print "File not found: %s" % filename
            return
        parser = parser_cls(filename)
        count = 0
        for item in parser.items:
            if insert_item(project_name, parser, item):
                count += 1
            if count % 100 == 0:
                msg = "Inserted %d events..." % count
                sys.stdout.write(msg)
                sys.stdout.flush()
                sys.stdout.write('\b' * len(msg))
        sys.stdout.write("Inserted %d events...\n" % count)


class ListParsers(Command):
    """
    Lists currently available parser types.
    """
    def run(self):
        print "Available parsers:"
        for parser_name in get_parser_names():
            print '*', parser_name


class DropDB(Command):
    """
    Drops database for given project.
    """
    option_list = (
        Option('-p', '--project', dest='project', required=True),
    )

    def run(self, project):
        if not project in get_database_names():
            print "No such project: %s" % project
            return
        connection.drop_database(project)
        print "Dropped '%s' project" % project


manager = Manager(app)
manager.add_command('load_data', LoadData())
manager.add_command('list_parsers', ListParsers())
manager.add_command('drop_db', DropDB())
manager.run()
