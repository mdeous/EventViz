# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from eventviz.db import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', page='home')


@main.route('/timeline')
def timeline():
    data = []
    for db_item in db['apache_access'].find():
        item = {'start': db_item['time'].strftime('%a, %d %b %Y %H:%M:%S'),
                'content': '%s %s' % (db_item['method'], db_item['querystring'])}
        data.append(item)
    return render_template(
        'timeline.html',
        data=data,
        page='timeline'
    )
