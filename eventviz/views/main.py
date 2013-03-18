# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, url_for, redirect

from eventviz.db import connection, get_database_names, get_projects_stats

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

@main.route('/timeline/<string:project>')
def project_timeline(project):
    if project not in get_database_names():
        # TODO: send flash message
        return redirect(url_for('main.timeline'))
    db = connection[project]
    data = []
    for db_item in db['apache_access'].find():
        item = {'start': db_item['time'].strftime('%a, %d %b %Y %H:%M:%S'),
                'content': '%s %s' % (db_item['method'], db_item['querystring'])}
        data.append(item)
    return render_template(
        'prj_timeline.html',
        page='timeline',
        data=data
    )
