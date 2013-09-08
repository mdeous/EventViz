# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for

import eventviz
from eventviz.db import get_fieldnames, get_exact_matches, get_event_types, get_containing_matches, get_regex_matches
from eventviz.lib.parsers import get_parser_by_name

search = Blueprint('search', __name__)
SEARCH_FUNCS = {
    'equals': get_exact_matches,
    'contains': get_containing_matches,
    'regex': get_regex_matches
}


@search.route('/', methods=['GET', 'POST'])
def index():
    project = eventviz.project
    if project is None:
        # TODO: send flash message
        return redirect(url_for('main.index'))
    results = []
    result_fields = []
    filters = None
    if request.method == 'POST':
        for form_field in ('search-field', 'search-type', 'search-etype', 'query'):
            if form_field not in request.form:
                # TODO: send flash message
                return redirect(url_for('search.index', project=project))
        # TODO: validate input
        if request.form['search-type'] not in SEARCH_FUNCS:
            # TODO send flash message
            return redirect(url_for('search.index'))
        results = SEARCH_FUNCS[request.form['search-type']](
            project,
            request.form['search-etype'],
            request.form['search-field'],
            request.form['query']
        )
        result_fields = get_parser_by_name(request.form['search-etype']).fieldnames
        filters = {
            'event_type': request.form['search-etype'],
            'field': request.form['search-field'],
            'search_type': request.form['search-type'],
            'query': request.form['query']
        }

    return render_template(
        'search.html',
        page='search',
        project=project,
        fields=get_fieldnames(project),
        event_types=get_event_types(project),
        results=results,
        result_fields=result_fields,
        filters=filters
    )
