from flask import Blueprint, render_template, request, redirect, url_for, session
from json import dumps, loads
from extensions import mysql as con, marked, dict_cursor, get_cursor, \
    stm_update_user, stm_check_user, stm_update_user_preferences
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
            elif not re.match(r'[A-Za-z0-9_]*$', uname):
                # if username doesn't meet requirements, don't update
                msg = 'Username must be letters, numbers and underscores only.'
            else:
                # if account did not exist and the username is okay, update the
                # username and your session variable
                cur.execute(stm_update_user, (uname, uid))
                con.connection.commit()
                msg = 'Account updated successfully.'
                session['username'] = uname

            return render_template(
                'settings/username.html',
                username=session['username'],
                msg=msg)

    else:
        return redirect(url_for('view.home'))

@setting_bp.route('/home-filters', methods=['GET','POST'])
def home_filters():
    if 'loggedin' in session:
        if request.method == 'GET':
            return render_template('settings/home-filters.html')
        elif request.method == 'POST':
            # get the specified setting 
            pref = request.form['home-pg-filter']
            usettings = session['user-preferences']
            usettings['home-pg-filter'] = pref
            new_settings = dumps(usettings)

            # save the new settings
            cur = get_cursor()
            arg = (new_settings, session['id'])
            cur.execute(stm_update_user_preferences, arg)
            cur.connection.commit()

            # update the session and let the user know the update succeeded
            msg = 'Home page preference updated successfully.'
            session['user-preferences'] = usettings
            return render_template('settings/home-filters.html', msg=msg)
            
    else:
        return redirect(url_for('view.home'))
