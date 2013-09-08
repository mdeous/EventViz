# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, redirect

import eventviz
from eventviz import settings
from eventviz.db import connection, get_fieldnames, get_event_types, get_item

timeline = Blueprint('timeline', __name__)


@timeline.route('/', methods=['GET', 'POST'])
def index():
    project = eventviz.project
    if project is None:
        # TODO: send flash message
        return redirect(url_for('main.index'))
    db = connection['eventviz_%s' % project]
    available_fields = get_fieldnames(project)
    displayed_fields = ['method', 'querystring']
    group = None
    if request.method == 'POST':
        form_fields = request.form.getlist('fields')
        if form_fields:
            displayed_fields = form_fields
        if 'group' in request.form:
            group = request.form['group']
            if group == 'event_type':
                group = None
    data = []
    events = []
    for event_type in get_event_types(project):
        for db_item in db[event_type].find():
            db_item_id = str(db_item['_id'])
            item = {
                'start': db_item['time'].strftime(settings.JS_DATE_FORMAT),
                'group': db_item.get(group, 'E_NOGROUP') if group is not None else event_type,
                'content': ' - '.join(map(lambda f: str(db_item.get(f, 'N/A')), displayed_fields)),
                'className': '%s eventtype-%s' % (db_item_id, event_type)
            }
            data.append(item)
            events.append(db_item_id)
    events.append('event_type')
    filters = {
        'fields': ','.join(displayed_fields),
        'group_by': group or 'event_type'
    }
    return render_template(
        'timeline.html',
        page='timeline',
        project=project,
        event_fields=available_fields,
        data=data,
        events=events,
        filters=filters
    )

@timeline.route('/<string:event_type>/<string:event_id>')
def event_details(event_type, event_id):
    if event_type not in get_event_types(eventviz.project):
        return redirect(url_for('timeline.index'))
    event = get_item(eventviz.project, event_type, event_id)
    del event['_id']
    return render_template('event_details.html', event=event)
