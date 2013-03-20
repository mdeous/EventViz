# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

search = Blueprint('search', __name__)


@search.route('/', methods=['GET', 'POST'])
def index():
    return render_template(
        'search/index.html',
        page='search',
        results=[]
    )
