# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for

import eventviz
from eventviz.db import get_projects_stats, get_database_names

main = Blueprint('main', __name__)


@main.route('/')
def index():
    project = request.args.get('project')
    stats = get_projects_stats()
    stats['__total_events'] = sum(stats.values())
    if project is not None:
        if project not in get_database_names():
            # TODO: send flash message
            return redirect(url_for('main.index'))
        eventviz.project = project
        return redirect(url_for('timeline.index'))
    return render_template(
        'index.html',
        page='home',
        current_prj=eventviz.project,
        stats=stats
    )
