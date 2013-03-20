# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from eventviz.db import get_projects_stats

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
