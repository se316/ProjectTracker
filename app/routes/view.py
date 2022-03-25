from flask import Blueprint, render_template, request, redirect, url_for, session
from json import loads
from datetime import datetime
from extensions import mysql as con, marked, dict_cursor, get_cursor, \
    stm_login, stm_projects, stm_subtasks, stm_select_project, \
    stm_select_subtask, stm_comments, stm_new_comment


view_bp = Blueprint(
    'view',
    __name__,
    url_prefix='/view',
    template_folder='templates')


@view_bp.context_processor
def status_list():
    """
    used to return a list of statuses, accessible at the template level
    """
    statuses = [
    'Not Started',
    'Pending',
    'In Progress',
    'Blocked',
    'Researching',
    'Review',
    'Complete',
    'Closed',
    'Backlog'
    ]
    return {'status_list' : statuses}


@view_bp.route('/')
def home():
    """
    The home page containing a list of projects
    """
    if 'loggedin' in session:
        uname = session['username']
        no_projects = 'No projects created. To start a new project, select New Project in the upper right hand corner!'
        uid = session['id']
        session['current-project'] = None
        session['current-subtask'] = None
        cursor = con.connection.cursor(dict_cursor)
        cursor.execute(stm_projects, (uid,))
        projects = cursor.fetchall()
        if projects:
            for proj in projects:
                proj['pdescription'] = marked(proj['pdescription'])
            return render_template(
                'home.html',
                projects=projects,
                no_projects=no_projects,
                username=uname)
        else:
            return render_template(
                'home.html',
                projects=None,
                no_projects=no_projects,
                username=uname)
    else:
        return redirect(url_for('.login'))


@view_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    the login page
    """
    msg = ''
    # get user/pass from submission
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # check if account exists in db
        cursor = con.connection.cursor(dict_cursor)
        cursor.execute(stm_login, (username, password))
        # get account data from query
        account = cursor.fetchone()

        # if account was returned
        if account:
            # create session data, this can be accessed by other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['current-project'] = None
            session['current-subtask'] = None
            session['user-preferences'] = loads(account['settings'])
            # redirect to the home page
            return redirect(url_for('.home'))

        # if there was not a user/pass match in the db
        else:
            msg = 'Incorrect username/password was provided.'

    return render_template('index.html', msg=msg)


@view_bp.route('/subtask/<stid>/comments', methods=['GET', 'POST'])
def comments(stid):
    """
    Shows the comments for a given subtask
    """
    if 'loggedin' in session:
        if request.method == 'GET':
            uid = session['id']
            session['current-subtask'] = stid
            cursor = get_cursor()
            # get args for comments and the subtask
            cm_args = (uid, stid)
            # get the subtask, if it exists
            cursor.execute(stm_select_subtask, cm_args)
            subtask = cursor.fetchone()
            # get the comments for the subtask, if they exist
            cursor.execute(stm_comments, cm_args)
            comments = cursor.fetchall()
            # render markdown for subtask descriptions
            if subtask:
                if comments:
                    for cm in comments:
                        comments[comments.index(cm)]['comment'] = marked(
                            cm['comment'])
                return render_template(
                    'comments.html', subtask=subtask, comments=comments)
            else:
                return '<p>404, a subtask was not found with the id that matches your account.</p>'
        elif request.method == 'POST':
            # get and prep the arguments
            uid = session['id']
            comment = request.form['comment']
            create_time = str(datetime.now())[:19]  # YYYY-MM-DD HH:MM:SS
            entry = [stid, uid, comment, create_time, create_time]
            # get a cursor and add the new entry, commit the change
            cursor = get_cursor()
            cursor.execute(stm_new_comment, entry)
            con.connection.commit()
            # return user to the comments view
            return redirect(url_for('view.comments', stid=stid))

            return 0
    else:
        return redirect(url_for('.login'))


@view_bp.route('/subtask/<stid>')
def subtask(stid):
    """
    Returns the individual subtask page
    """
    if 'loggedin' in session:
        # get the user_id, subtask id is provided
        uid = session['id']
        cursor = get_cursor()
        cursor.execute(stm_select_subtask, (uid, stid))
        subtask = cursor.fetchone()
        if subtask:
            # get args for comments
            cm_args = (uid, stid)
            # get the comments for the subtask, if they exist
            cursor.execute(stm_comments, cm_args)
            comments = cursor.fetchall()
            session['current-subtask'] = stid
            # render markdown for subtask descriptions
            if comments:
                for cm in comments:
                    comments[comments.index(cm)]['comment'] = marked(
                        cm['comment'])
            # render markdown in the description
            subtask['stdescription'] = marked(subtask['stdescription'])
            return render_template(
                'subtask.html',
                active='subtask_view',
                subtask=subtask,
                comments=comments)
        else:
            return '<h2>404, project was not found for your account</h2>'
    else:
        return redirect(url_for('.login'))


@view_bp.route('/project/<projid>')
def project(projid):
    """
    Returns the individual project page
    """
    if 'loggedin' in session:
        # get the user_id, project id is provided
        uid = session['id']
        cursor = get_cursor()
        cursor.execute(stm_select_project, (uid, projid))
        project = cursor.fetchone()
        if project:
            # save the current proj. id to use for subtask creation
            pid = project['pid']
            session['current-project'] = pid
            session['project-title'] = project['pname']
            st_args = (uid, pid)
            # get the subtasks for the project, if they exist
            cursor.execute(stm_subtasks, st_args)
            subtasks = cursor.fetchall()
            # render markdown for subtask descriptions
            if subtasks:
                for st in subtasks:
                    subtasks[subtasks.index(st)]['stdescription'] = marked(
                        st['stdescription'])
            # render markdown in the description
            project['pdescription'] = marked(project['pdescription'])
            return render_template(
                'project.html',
                project=project,
                subtasks=subtasks)
        else:
            return '<h2>404, project was not found for your account</h2>'
    else:
        return redirect(url_for('.login'))


@view_bp.route('/logout')
def logout():
    """
    log out a user
    """
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('current-project', None)
    # redirect to login page
    return redirect(url_for('.login'))
