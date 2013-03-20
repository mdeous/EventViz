# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request

from eventviz.db import get_database_names, connection, get_projects_stats
from eventviz.lib.parsers import get_parser_by_name

timeline = Blueprint('timeline', __name__)


@timeline.route('/')
def index():
    return render_template(
        'timeline/index.html',
        page='timeline',
        stats=get_projects_stats()
    )

@timeline.route('/<string:project>', methods=['GET', 'POST'])
def project(project):
    if project not in get_database_names():
        # TODO: send flash message
        return redirect(url_for('timeline.index'))
    db = connection[project]
    event_types = db.collection_names()
    event_types.remove('system.indexes')
    available_fields = set()
    displayed_fields = ['method', 'querystring']
    group = None
    if request.method == 'POST':
        form_fields = request.form.getlist('fields')
        if form_fields:
            displayed_fields = form_fields
        if 'group' in request.form:
            group = request.form['group']
    data = []
    for event_type in event_types:
        available_fields.update(get_parser_by_name(event_type).fieldnames)
        for db_item in db[event_type].find():
            item = {
                'start': db_item['time'].strftime('%a, %d %b %Y %H:%M:%S'),
                'group': db_item.get(group) or event_type,
                'content': ' - '.join(map(lambda f: db_item.get(f, ''), displayed_fields))
            }
            data.append(item)
    return render_template(
        'timeline/project.html',
        page='timeline',
        project=project,
        event_fields=available_fields,
        data=data
    )