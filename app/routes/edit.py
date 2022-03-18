from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import mysql as con, marked, dict_cursor, get_cursor, \
        stm_login, stm_projects, stm_delete_project, stm_select_project, stm_select_subtask, \
        stm_select_comment, stm_update_project, stm_update_subtask, stm_update_comment, \
        stm_update_status_project, stm_update_status_subtask

from datetime import datetime


update_bp = Blueprint('edit', __name__, url_prefix='/edit', template_folder='templates')

@update_bp.route('/status/<level>/<id>', methods=['POST'])
def status(level, id):
    """
    Update the status of a project or subtask, this is meant to be triggered by JS fetch request.
    """
    if 'loggedin' in session:
        if request.method == 'POST':
            # get the data needed to make an update
            uid = session['id']
            status = request.form['status']
            update_time = str(datetime.now())[:19]
            if status == 'Complete':
                cstatus = status
            else:
                cstatus = ''
            entry = [status, update_time, cstatus, uid, id]

            # get a cursor
            cursor = get_cursor()

            # figure out where this update goes
            if level == 'project':
                cursor.execute(stm_update_status_project, entry)
            elif level == 'subtask':
                cursor.execute(stm_update_status_subtask, entry)

            # commit the change
            con.connection.commit()
            return 'OK'
    else:
        return redirect(url_for('view.login'))

@update_bp.route('/project/<projid>', methods=['GET','POST'])
def project(projid):
    """
    Edit a given project id
    """
    if 'loggedin' in session:
        # if a get request, give the user the current project title/description
        if request.method == 'GET':
            uid = session['id']
            cursor = con.connection.cursor(dict_cursor)

            # use the user id and project id to retrieve the project
            cursor.execute(stm_select_project, (uid,projid,))
            project = cursor.fetchone()

            # pass the values to the project editor template
            return render_template('edit-project.html', project=project, msg='')
        # if the user is submitting information, update the db with the modified entries
        # and update the last_modified_time val
        elif request.method == 'POST':
            uid = session['id']
            update_time = str(datetime.now())[:19]
            cursor = con.connection.cursor(dict_cursor)

            # prep args to be updated and matched against
            update_args = [
                    request.form['ptitle'],
                    request.form['pdescription'],
                    update_time,
                    uid,
                    projid]

            # update entry that matches `user_id` and `pid`
            cursor.execute(stm_update_project, update_args)
            con.connection.commit()

            return redirect(url_for('view.project', projid=projid))
    else:
        return redirect(url_for('view.login'))

@update_bp.route('/subtask/<stid>', methods=['GET','POST'])
def subtask(stid):
    """
    Edit a given subtask id
    """
    if 'loggedin' in session:
        uid = session['id']
        # if a get request, give the user the current subtask title/description
        if request.method == 'GET':
            # use the user id and subtask id to retrieve the project
            cursor = get_cursor()
            cursor.execute(stm_select_subtask, (uid,stid))
            subtask = cursor.fetchone()
            session['current-project'] = subtask['pid']
            pid = subtask['pid']

            # pass the values to the project editor template
            return render_template('edit-subtask.html', subtask=subtask, pid=pid, msg='')

        # if the user is submitting information, update the db with the modified entries
        # and update the last_modified_time val
        elif request.method == 'POST':
            uid = session['id']
            pid = session['current-project']
            update_time = str(datetime.now())[:19]
            cursor = get_cursor()

            # prep args to be updated and matched against
            update_args = [
                    request.form['stname'],
                    request.form['stdescription'],
                    update_time,
                    uid,
                    stid]

            # update entry that matches `user_id` and `pid`
            cursor.execute(stm_update_subtask, update_args)
            con.connection.commit()

            return redirect(url_for('view.subtask', stid=stid))
    else:
        return redirect(url_for('view.login'))

@update_bp.route('/comment/<cmid>', methods=['GET','POST'])
def comment(cmid):
    """
    Edit a given comment id
    """
    if 'loggedin' in session:
        uid = session['id']
        stid = session['current-subtask']
        # if a get request, give the user the current comment
        if request.method == 'GET':
            # use the user id and comment id for retrieving comment
            cursor = get_cursor()
            cursor.execute(stm_select_comment, (uid,cmid))
            comment = cursor.fetchone()

            # pass the values to the project editor template
            return render_template('edit-comment.html', comment=comment, msg='')

        # if the user is submitting information, update the db with the modified entries
        # and update the last_modified_time val
        elif request.method == 'POST':
            update_time = str(datetime.now())[:19]
            cursor = get_cursor()

            # prep args to be updated and matched against
            update_args = [
                    request.form['comment'],
                    update_time,
                    uid,
                    cmid]

            # update entry that matches `user_id` and `cmid`
            cursor.execute(stm_update_comment, update_args)
            con.connection.commit()

            return redirect(url_for('view.comments', stid=stid))
    else:
        return redirect(url_for('view.login'))
