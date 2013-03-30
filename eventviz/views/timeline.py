# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, redirect

import eventviz
from eventviz import settings
from eventviz.db import connection, get_fieldnames, get_event_types

timeline = Blueprint('timeline', __name__)


@timeline.route('/', methods=['GET', 'POST'])
def index():
    project = eventviz.project
    if project is None:
        # TODO: send flash message
        return redirect(url_for('main.index'))
    db = connection[project]
    available_fields = get_fieldnames(project)
    displayed_fields = ['method', 'querystring']
    group = None
    if request.method == 'POST':
        form_fields = request.form.getlist('fields')
        if form_fields:
            displayed_fields = form_fields
        if 'group' in request.form:
            group = request.form['group']
    data = []
    for event_type in get_event_types(project):
        for db_item in db[event_type].find():
            item = {
                'start': db_item['time'].strftime(settings.JS_DATE_FORMAT),
                'group': db_item.get(group, 'N/A') if group is not None else event_type,
                'content': ' - '.join(map(lambda f: str(db_item.get(f, 'N/A')), displayed_fields))
            }
            data.append(item)
    return render_template(
        'timeline.html',
        page='timeline',
        project=project,
        event_fields=available_fields,
        data=data
    )
