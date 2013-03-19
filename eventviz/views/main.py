# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, url_for, redirect, request

from eventviz.db import connection, get_database_names, get_projects_stats
from eventviz.lib.parsers import get_parser_by_name

main = Blueprint('main', __name__)


@main.route('/')
def index():
    stats = get_projects_stats()
    stats['__total_events'] = sum(stats.values())
    return render_template(
        'index.html',
        page='home',
        stats=stats
    )

@main.route('/timeline')
def timeline():
    return render_template(
        'timeline.html',
        page='timeline',
        stats=get_projects_stats()
    )

@main.route('/timeline/<string:project>', methods=['GET', 'POST'])
def project_timeline(project):
    if project not in get_database_names():
        # TODO: send flash message
        return redirect(url_for('main.timeline'))
    db = connection[project]
    event_types = db.collection_names()
    event_types.remove('system.indexes')
    fixed_fields = set()
    displayed_fields = ['method', 'querystring']
    if request.method == 'POST':
        displayed_fields = request.form.getlist('fields')
    data = []
    for event_type in event_types:
        fixed_fields.update(get_parser_by_name(event_type).fixed_fields)
        for db_item in db[event_type].find():
            print db_item
            item = {
                'start': db_item['time'].strftime('%a, %d %b %Y %H:%M:%S'),
                'group': event_type,
                'content': ' - '.join(map(lambda f: db_item.get(f), displayed_fields))
            }
            data.append(item)
    return render_template(
        'prj_timeline.html',
        page='timeline',
        project=project,
        event_fields=fixed_fields,
        data=data
    )
