# -*- coding: utf-8 -*-

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
    dbs.remove('local')
    return dbs


@cache()
def get_event_types(db_name):
    db = connection[db_name]
    event_types = db.collection_names()
    event_types.remove('system.indexes')
    return event_types


@cache()
def get_projects_stats():
    stats = {}
    for project in get_database_names():
        db = connection[project]
        total_events = sum(db[coll].count() for coll in get_event_types(project))
        stats[project] = total_events
    return stats


@cache()
def get_fieldnames(db_name):
    fieldnames = set()
    db = connection[db_name]
    event_types = db.collection_names()
    event_types.remove('system.indexes')
    for event_type in event_types:
        fieldnames.update(get_parser_by_name(event_type).fieldnames)
    return fieldnames


@cache()
def get_exact_matches(db_name, coll_name, fieldname, value):
    db = connection[db_name]
    coll = db[coll_name]
    return list(coll.find({fieldname: value}, fields={'_id': False}))


@cache()
def get_item(db_name, coll_name, item_id):
    db = connection[db_name]
    coll = db[coll_name]
    return coll.find_one(ObjectId(item_id))


def insert_item(db_name, parser, data):
    if db_name == 'local':
        raise ValueError("Can't insert data into 'local' database")
    collection = connection[db_name][parser.name]
    for index in parser.base_indexes:
        collection.ensure_index([(index[0], pymongo.ASCENDING)], unique=index[1], drop_dups=index[1])
    for index in parser.extra_indexes:
        collection.ensure_index([(index[0], pymongo.ASCENDING)], unique=index[1], drop_dups=index[1])
    try:
        collection.insert(data)
    except DuplicateKeyError:
        return False
    return True
