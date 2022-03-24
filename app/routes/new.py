from pdb import set_trace
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import mysql as con, marked, dict_cursor, get_cursor, \
    stm_login, stm_projects, stm_select_project, stm_new_project, \
    stm_new_subtask, stm_check_user, stm_add_user
import re

new_bp = Blueprint(
    'new',
    __name__,
    url_prefix='/new',
    template_folder='templates')


@new_bp.route('/account', methods=['GET', 'POST'])
def account():
    """
    Create a new user account
    """
    # error message in case something's wrong
    msg = ''
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            # assign to variables for easy access
            uname = request.form['username']
            pword = request.form['password']

            # check if a user exists with that name
            cursor = get_cursor()
            cursor.execute(stm_check_user, (uname,))
            account = cursor.fetchone()

            # if account exists, show error and validation checks
            if account:
                msg = 'Account already exists for this username.'
            elif not re.match(r'[A-Za-z0-9_]*$', uname):
                msg = 'Username must be letters, numbers and underscores only.'
            elif not uname or not pword:
                msg = 'Please fill out both fields in the form.'
            else:
                # account does not exist and data is valid at this point
                cursor.execute(stm_add_user, (uname, pword))
                con.connection.commit()
                msg = 'Successfully registered user: {}'.format(uname)
                return render_template('index.html', msg=msg)

            # if we didn't take the else branch, return the template with the
            # message
        return render_template('register.html', msg=msg)


@new_bp.route('/subtask', methods=['GET', 'POST'])
def subtask():
    """
    Subtask creation page.
    """
    if 'loggedin' in session:
        msg = ''
        current_project = session['current-project']
        title = session['project-title']
        if request.method == 'GET':
            return render_template(
                'new-subtask.html',
                msg=msg,
                project_title=title,
                current_project=current_project)
        elif request.method == 'POST':
            print(request.form)
            stname = request.form['stname']
            # check if a description was given, not required
            if 'stdescription' in request.form:
                stdesc = request.form['stdescription']
            else:
                stdesc = ''
            # set initial status and create time
            ststatus = 'Not Started'
            create_time = str(datetime.now())[:19]  # YYYY-MM-DD HH:MM:SS
            # (pid, user_id, stname, stdescription, ststatus, create_time, last_modified_time, complete_time)
            entry = [
                session['current-project'],
                session['id'],
                stname,
                stdesc,
                ststatus,
                create_time,
                create_time,
                ''
            ]

            # add the new subtask to the db
            cursor = get_cursor()
            cursor.execute(stm_new_subtask, entry)
            con.connection.commit()

            # return back to the project view
            return redirect(
                url_for(
                    'view.project',
                    projid=session['current-project']))

    else:
        return redirect(url_for('view.login'))


@new_bp.route('/project', methods=['GET', 'POST'])
def project():
    """
    Project creation page
    """
    if 'loggedin' in session:
        msg = ''
        if request.method == 'POST' and 'ptitle' in request.form:

            # prep your variables for the sql insert statement, need the following
            # pid, (user_id, pname, pdescription, pstatus, create_time, last_modified_time, completed_time)
            uid = session['id']
            pname = request.form['ptitle']

            # descriptions are ideal, but not neccessary for creating a project
            if 'pdescription' in request.form:
                pdescription = request.form['pdescription']
            else:
                pdescription = ''
            pstatus = 'Not Started'
            create_time = str(datetime.now())[:19]  # YYYY-MM-DD HH:MM:SS
            project_data = [
                uid,
                pname,
                pdescription,
                pstatus,
                create_time,
                create_time,
                '']

            # save the project data to the db
            cursor = get_cursor()
            cursor.execute(stm_new_project, project_data)
            con.connection.commit()

            # Return to the home page
            return redirect(url_for('view.home'))

        elif request.method == 'POST':
            msg = 'You must include a title.'
            return render_template('new-project.html', msg=msg)

        elif request.method == 'GET':
            return render_template('new-project.html', msg=msg)
        return render_template('new-project.html', msg=msg)

    else:
        return redirect(url_for('view.login'))
