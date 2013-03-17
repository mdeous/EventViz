# -*- coding: utf-8 -*-


import pymongo
from pymongo.errors import DuplicateKeyError

from eventviz import settings


connection = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = connection[settings.MONGO_DB]


def insert_item(parser, data):
    collection = db[parser.name]
    for index in parser.base_indexes:
        collection.ensure_index([(index[0], pymongo.ASCENDING)], unique=index[1], drop_dups=index[1])
    for index in parser.extra_indexes:
        collection.ensure_index([(index[0], pymongo.ASCENDING)], unique=index[1], drop_dups=index[1])
    try:
        collection.insert(data)
    except DuplicateKeyError:
        return False
    return True