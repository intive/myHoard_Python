import subprocess

from flask import current_app, render_template


def current_revision():
    return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])


def landingpage():
    links = []
    for rule in current_app.url_map.iter_rules():
        links.append((rule.endpoint, str(rule), list(rule.methods)))

    return render_template('index.html', links=sorted(links),
                           revision=current_revision())