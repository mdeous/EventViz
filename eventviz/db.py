# -*- coding: utf-8 -*-

import re

import pymongo
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

from eventviz import settings
from eventviz.lib.parsers import get_parser_by_name
from eventviz.lib.utils import cache


connection = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)


@cache()
def get_database_names():
    dbs = connection.database_names()
    return [db[9:] for db in dbs if db[:9] == 'eventviz_']


@cache()
def get_event_types(project_name):
    project_name = 'eventviz_%s' % project_name
    db = connection[project_name]
    event_types = db.collection_names()
    return event_types


@cache()
def get_projects_stats():
    stats = {}
    for project in get_database_names():
        print project
        db = connection[project]
        total_events = sum(db[coll].count() for coll in get_event_types(project))
        stats[project] = total_events
    return stats


@cache()
def get_fieldnames(project_name):
    fieldnames = set()
    project_name = 'eventviz_%s' % project_name
    db = connection[project_name]
    event_types = db.collection_names()
    event_types.remove('system.indexes')
    for event_type in event_types:
        fieldnames.update(get_parser_by_name(event_type).fieldnames)
    return fieldnames


@cache()
def get_exact_matches(project_name, coll_name, fieldname, value):
    project_name = 'eventviz_%s' % project_name
    db = connection[project_name]
    coll = db[coll_name]
    return list(coll.find({fieldname: value}, fields={'_id': False}))


def get_containing_matches(project_name, coll_name, fieldname, value):
    # NOTE: returns a generator, not cachable
    project_name = 'eventviz_%s' % project_name
    db = connection[project_name]
    coll = db[coll_name]
    for item in coll.find(fields={'_id': False}):
        if value in item[fieldname]:
            yield item


def get_regex_matches(project_name, coll_name, fieldname, value):
    # NOTE: returns a generator, not cachable
    project_name = 'eventviz_%s' % project_name
    db = connection[project_name]
    coll = db[coll_name]
    regex = re.compile(value)
    for item in coll.find(fields={'_id': False}):
        if regex.search(item[fieldname]) is not None:
            yield item


@cache()
def get_item(project_name, coll_name, item_id):
    project_name = 'eventviz_%s' % project_name
    db = connection[project_name]
    coll = db[coll_name]
    return coll.find_one(ObjectId(item_id))


def insert_item(project_name, parser, data):
    project_name = 'eventviz_%s' % project_name
    collection = connection[project_name][parser.name]
    try:
        collection.insert(data)
    except DuplicateKeyError:
        return False
    return True


def setup_indexes():
    for db in get_database_names():
        if 'eventviz_' in db:
            for collection in get_event_types(db):
                parser = get_parser_by_name(collection)
                for index in parser.indexes:
                    connection[db][collection].ensure_index(
                        index['field'],
                        unique=index['unique'],
                        drop_dups=index['unique']
                    )
