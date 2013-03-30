# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for

import eventviz
from eventviz import settings
from eventviz.db import get_fieldnames, get_exact_matches, get_event_types
from eventviz.lib.parsers import get_parser_by_name

search = Blueprint('search', __name__)


@search.route('/', methods=['GET', 'POST'])
def index():
    project = eventviz.project
    if project is None:
        # TODO: send flash message
        return redirect(url_for('main.index'))
    results = []
    result_fields = []
    if request.method == 'POST':
        for form_field in ('search-field', 'search-type', 'search-etype', 'query'):
            if form_field not in request.form:
                # TODO: send flash message
                return redirect(url_for('search.project', project=project))
        # TODO: validate input
        if request.form['search-type'] == 'equal':
            results = get_exact_matches(
                project,
                request.form['search-etype'],
                request.form['search-field'],
                request.form['query']
            )
            result_fields = get_parser_by_name(request.form['search-etype']).fieldnames
            for result in results:
                result['time'] = result['time'].strftime(settings.JS_DATE_FORMAT)

    return render_template(
        'search.html',
        page='search',
        project=project,
        fields=get_fieldnames(project),
        event_types=get_event_types(project),
        results=results,
        result_fields=result_fields
    )
