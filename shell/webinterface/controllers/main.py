from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_security import current_user

from shell.webinterface.extensions import cache

main = Blueprint('main', __name__)


@main.route('/')
#@cache.cached(timeout=1000)
def home():
    return render_template('main/index.html',
                           current_user=current_user)
