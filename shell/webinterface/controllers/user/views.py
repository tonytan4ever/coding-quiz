from flask import (Blueprint, render_template, flash, request, redirect, url_for,
                   current_app)
from flask_security import login_required, current_user

user = Blueprint('user', __name__)


@user.route('/profile')
@login_required
def profile():
    social = current_app.extensions['social']
    return render_template(
        'user/profile.html',
        #content='Profile Page',
        twitter_conn=social.twitter.get_connection(),
        facebook_conn=social.facebook.get_connection()
        #foursquare_conn=social.foursquare.get_connection()
        )