from flask_mysqldb import MySQL
from mdx_gfm import GithubFlavoredMarkdownExtension as gfme
from os import listdir
import MySQLdb.cursors
import logging
import markdown
from json import dumps
logging.basicConfig(level='INFO')

# re-usable connection object among app and blueprints
mysql = MySQL()

# re-usable cursor object for executing queries
dict_cursor = MySQLdb.cursors.DictCursor

# default settings for a user
default_settings = {
        'home-pg-filter':'all'
        }

# re-usable sql queries
stm_login = 'SELECT * FROM accounts WHERE username = %s AND password = %s;'
stm_check_user = 'SELECT * FROM accounts WHERE username = %s;'
stm_add_user = 'INSERT INTO accounts (username, password, settings) VALUES (%s, %s, %s);'
# -- select all entries related to a certain id
stm_projects = """
SELECT * FROM projects
 WHERE user_id = "%s"
 ORDER BY (
             CASE pstatus -- manual sort order via status
             WHEN 'In Progress' THEN 1
             WHEN 'Pending' THEN 2
             WHEN 'Review' THEN 3
             WHEN 'Researching' THEN 4
             WHEN 'Not Started' THEN 5
             WHEN 'Backlog' THEN 6
             WHEN 'Complete' THEN 7
             WHEN 'Closed' THEN 8
             WHEN 'Blocked' THEN 9
             END
         ),  last_modified_time DESC;
"""
stm_subtasks = 'SELECT * FROM subtasks WHERE user_id = "%s" AND pid=%s ORDER BY create_time;'
stm_comments = 'SELECT * FROM comments WHERE user_id = "%s" AND stid=%s ORDER BY create_time DESC;'
# -- add new entries at various levels
stm_new_project = """
INSERT INTO projects (user_id, pname, pdescription, pstatus, create_time, last_modified_time, completed_time)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""
stm_new_subtask = """
INSERT INTO subtasks (pid, user_id, stname, stdescription, ststatus, create_time, last_modified_time, completed_time)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""
stm_new_comment = """
INSERT INTO comments (stid, user_id, comment, create_time, last_modified_time)
VALUES (%s, %s, %s, %s, %s);
"""
# -- select individual entries by id
stm_select_project = 'SELECT * FROM projects WHERE user_id = %s AND pid = %s ;'
stm_select_subtask = 'SELECT * FROM subtasks WHERE user_id = %s AND stid = %s ;'
stm_select_comment = 'SELECT * FROM comments WHERE user_id = %s AND cmid = %s ;'
# -- update existing entries by id, need name description and last modded times filtered
#    by userid and level id (pid, stid, cmid)
stm_update_user = """
    UPDATE accounts
    SET username=%s
    WHERE id = %s;
"""
stm_update_project = """
    UPDATE projects
    SET pname=%s, pdescription=%s, last_modified_time=%s
    WHERE user_id = %s AND pid = %s;
    """
stm_update_subtask = """
    UPDATE subtasks
    SET stname=%s, stdescription=%s, last_modified_time=%s
    WHERE user_id = %s AND stid = %s;
    """
stm_update_comment = """
    UPDATE comments
    SET comment=%s, last_modified_time=%s
    WHERE user_id = %s AND cmid = %s;
    """
stm_update_status_project = """
    UPDATE projects
    SET pstatus=%s, last_modified_time=%s, completed_time=%s
    WHERE user_id = %s AND pid = %s;
"""
stm_update_status_subtask = """
    UPDATE subtasks
    SET ststatus=%s, last_modified_time=%s, completed_time=%s
    WHERE user_id = %s AND stid = %s;
"""
stm_update_user_preferences = """
    UPDATE accounts
    SET settings=%s
    WHERE id=%s;
"""
# -- delete existing entry by specific id
stm_delete_project = 'DELETE FROM projects WHERE user_id = %s AND pid = %s;'
stm_delete_subtask = 'DELETE FROM subtasks WHERE user_id = %s AND stid = %s;'
stm_delete_comment = 'DELETE FROM comments WHERE user_id = %s AND cmid = %s;'


# re-usable function for rendering markdown as Github flavored markdown html
def marked(txt):
    """
    clean way to render markdown
    """
    return markdown.markdown(txt, extensions=[gfme(), 'codehilite'])


def get_cursor():
    """
    clean way to get a cursor object
    """
    return mysql.connection.cursor(dict_cursor)
