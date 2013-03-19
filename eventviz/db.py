# -*- coding: utf-8 -*-


import pymongo
from pymongo.errors import DuplicateKeyError

from eventviz import settings


connection = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)


def get_database_names():
    dbs = connection.database_names()
    dbs.remove('local')
    return dbs


def get_projects_stats():
    stats = {}
    for project in get_database_names():
        db = connection[project]
        total_events = sum(db[coll].count() for coll in db.collection_names() if coll != 'system.indexes')
        stats[project] = total_events
    return stats


def insert_item(db, parser, data):
    if db not in get_database_names():
        raise ValueError("No such database: %s" % db)
    collection = connection[db]
    for index in parser.base_indexes:
        collection.ensure_index([(index[0], pymongo.ASCENDING)], unique=index[1], drop_dups=index[1])
    for index in parser.extra_indexes:
        collection.ensure_index([(index[0], pymongo.ASCENDING)], unique=index[1], drop_dups=index[1])
    try:
        collection.insert(data)
    except DuplicateKeyError:
        return False
    return True