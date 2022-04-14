from flask import Blueprint, render_template, request, redirect, url_for, session
from json import dumps, loads
from extensions import mysql as con, marked, dict_cursor, get_cursor, download, \
    stm_update_user, stm_check_user, stm_update_user_preferences, stm_login, stm_update_password
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


@setting_bp.route('/certificate')
def certificate():
    if 'loggedin' in session:
        return render_template('settings/certificate.html')
    else:
        return redirect(url_for('view.home'))

@setting_bp.route('/dl_cert')
def download_cert():
    loc = '/certs/rootcert/ca_crt.pem'
    return download(loc)

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

@setting_bp.route('/last_n_comments', methods=['GET','POST'])
def last_n_comments():
    if 'loggedin' in session:
        msg = ''
        # get user preferences
        usettings = session['user-preferences']
        if request.method == 'GET':
            # check if the setting exists, if not then set to 10
            if 'profile-n-comments' not in usettings:
                n_comments = 10
            else:
                n_comments = usettings['profile-n-comments']
            return render_template('settings/n-comments.html', n_comments=n_comments, msg=msg)
        elif request.method == 'POST':
            # get the amount and save in the preference copy
            try:
                n_comments = request.form['n-comments']
            except:
                # handle when user presses save but didn't select anything
                if 'profile-n-comments' not in usettings:
                    n_comments = 10
                else:
                    n_comments = usettings['profile-n-comments']

            usettings['profile-n-comments'] = n_comments
            new_settings = dumps(usettings)

            # save the new settings
            cur = get_cursor()
            arg = (new_settings, session['id'])
            cur.execute(stm_update_user_preferences, arg)
            cur.connection.commit()

            # update the session's variable and let user know the update succeeded
            msg = 'Last N comments updated successfully to {}.'.format(n_comments)
            session['user-preferences'] = usettings
            return render_template('settings/n-comments.html', msg=msg, n_comments=n_comments)

            return render_template('settings/n-comments.html', msg=msg)
    else:
        return redirect(url_for('view.home'))


@setting_bp.route('/password', methods=['GET','POST'])
def password():
    if 'loggedin' in session:
        msg = ''
        if request.method == 'GET':
            return render_template('settings/password.html', msg=msg)
        elif request.method == 'POST':
            # verify all the fields are filled out
            if all([arg in request.form for arg in ['old-password','new-password','new-password-verify']]):
                orig_pword = request.form['old-password']
                new_pword = request.form['new-password']
                new_pwordv = request.form['new-password-verify']
                uid = session['id']
                uname = session['username']

                # verify the new passwords are the same
                if new_pword != new_pwordv:
                    msg = 'Your new password should be the same in both fields.'
                    return render_template('settings/password.html', msg=msg)

                # verify the new password isn't the same as the original
                if new_pword == orig_pword:
                    msg = 'Your new password can\'t match the original password.'
                    return render_template('settings/password.html', msg=msg)

                # verify the original password is the correct one
                cur = get_cursor()
                cur.execute(stm_login, (uname, orig_pword))
                account = cur.fetchone()
                if not account:
                    msg = 'Your original password was incorrect.'
                    return render_template('settings/password.html', msg=msg)
                else:
                    # the creds are correct and new passwords match
                    # set the new password
                    cur.execute(stm_update_password, (new_pword, uid))
                    con.connection.commit()
                    msg = 'Password updated successfully.'
                    return render_template('settings/password.html', msg=msg)

            else:
                # if a field is missing say it needs to be filled out
                msg = 'Please fill out all the fields.'
                return render_template('settings/password.html', msg=msg)

            return render_template('settings/password.html')
    else:
        return redirect(url_for('view.home'))
