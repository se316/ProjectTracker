from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import mysql as con, marked, stm_login, stm_projects, dict_cursor, get_cursor, \
        stm_delete_project, stm_delete_subtask, stm_delete_comment


delete_bp = Blueprint('delete', __name__, url_prefix='/delete', template_folder='templates')
@delete_bp.route('/project/<projid>')
def project(projid):
    """
    Delete a given project id
    """
    if 'loggedin' in session:
        # get user id and cursor object
        uid = session['id']
        cursor = con.connection.cursor(dict_cursor)

        # use the user id and project id to delete the project
        cursor.execute(stm_delete_project, (uid,projid))
        con.connection.commit()

        # redirect to home page
        return redirect(url_for('view.home'))
    else:
        return redirect(url_for('view.login'))

@delete_bp.route('/subtask/<stid>')
def subtask(stid):
    """
    Delete a given subtask id
    """
    if 'loggedin' in session:
        # get user id and cursor object
        uid = session['id']
        cursor = get_cursor()

        # use the user id and project id to delete the subtask
        cursor.execute(stm_delete_subtask, (uid,stid))
        con.connection.commit()

        # redirect to home page
        return redirect(url_for('view.project', projid=session['current-project']))
    else:
        return redirect(url_for('view.login'))

@delete_bp.route('/comment/<cmid>')
def comment(cmid):
    """
    Delete a given subtask id
    """
    if 'loggedin' in session:
        # get user id and cursor object
        uid = session['id']
        cursor = get_cursor()

        # use the user id and comment id to delete the comment
        cursor.execute(stm_delete_comment, (uid,cmid))
        con.connection.commit()

        # redirect to comments page
        return redirect(url_for('view.comments', stid=session['current-subtask']))
    else:
        return redirect(url_for('view.login'))
