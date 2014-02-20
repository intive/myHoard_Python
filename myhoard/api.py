# -*- coding: utf-8 -*-
import subprocess
from flask import current_app, render_template

__author__ = 'mkr'


def current_revision():
    """ Fetches current Git revision.
    """
    revision = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
    return revision


def landingpage():
    """ Simple view for landing page where user can see all existing API endpoints.
    """
    links = []
    for rule in current_app.url_map.iter_rules():
        links.append((rule.endpoint, str(rule), list(rule.methods)))
    return render_template('index.html', links=sorted(links), revision=current_revision())