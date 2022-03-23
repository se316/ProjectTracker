from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import mysql as con, marked, dict_cursor, get_cursor, \
    stm_update_user, stm_check_user
import re


setting_bp = Blueprint(
    'settings',
    __name__,
    url_prefix='/settings',
    template_folder='templates')


@setting_bp.route('/')
def page():
    if 'loggedin' in session:
        return render_template('settings.html')
    else:
        return redirect(url_for('view.home'))


@setting_bp.route('/username', methods=['GET', 'POST'])
def username():
    if 'loggedin' in session:

        if request.method == 'GET':
            uname = session['username']
            return render_template('settings/username.html', username=uname)

        if request.method == 'POST':
            # get the username from the form
            uname = request.form['username']
            uid = session['id']
            cur = get_cursor()

            # check if the username exists
            cur.execute(stm_check_user, (uname, ))
            account = cur.fetchone()
            if account:
                # if account exists, don't update
                msg = 'Account already exists for this username.'
            elif not re.match(r'[A-Za-z0-9]+', uname):
                # if username doesn't meet requirements, don't update
                msg = 'Username must be letters and numbers only.'
            else:
                # if account did not exist and the username is okay, update the
                # username and your session variable
                cur.execute(stm_update_user, (uname, uid))
                msg = 'Account updated successfully.'
                session['username'] = uname

            return render_template(
                'settings/username.html',
                username=session['username'],
                msg=msg)

    else:
        return redirect(url_for('view.home'))
