from flask_mysqldb import MySQL
from mdx_gfm import GithubFlavoredMarkdownExtension as gfme
from os import listdir
import MySQLdb.cursors
import logging
import markdown
from flask import send_file
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
stm_all_subtasks = 'SELECT * FROM subtasks WHERE user_id = "%s" ORDER BY create_time;'
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
stm_update_password = """
    UPDATE accounts
    SET password=%s
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

# -- statements run to remove everything a user has from the database
stm_delete_account = [
        'DELETE FROM accounts WHERE id = %s;',
        'DELETE FROM projects WHERE user_id = %s;',
        'DELETE FROM subtasks WHERE user_id = %s;',
        'DELETE FROM comments WHERE user_id = %s;'
        ]

# -- query for retrieving the stats table on profile page
stm_stats = """
SELECT *
-- first table gets project statuses
  FROM (SELECT p.pstatus, IFNULL(p.p_pct,0) AS p_pct, IFNULL(p.p_count,0) AS p_count,
               IFNULL(s.s_pct,0) AS s_pct, IFNULL(s.s_count, 0) AS s_count
          FROM (SELECT ststatus, COUNT(ststatus) AS s_count, 
                       COUNT(ststatus) / SUM(COUNT(ststatus)) over () * 100 AS s_pct 
                  FROM subtasks
                 WHERE user_id=%s
                 GROUP BY ststatus) s
    RIGHT JOIN (SELECT pstatus, COUNT(pstatus) AS p_count,
                       COUNT(pstatus) / SUM(COUNT(pstatus)) over () * 100 AS p_pct
                  FROM projects
                 WHERE user_id=%s
                 GROUP BY pstatus) p
            ON s.ststatus = p.pstatus

         UNION -- union joins the 2 tables together and removes duplicates

-- second table gets subtask statuses
        SELECT s.ststatus, IFNULL(p.p_pct,0) AS p_pct, IFNULL(p.p_count,0) AS p_count,
               IFNULL(s.s_pct,0) AS s_pct, IFNULL(s.s_count, 0) AS s_count
          FROM (SELECT ststatus, COUNT(ststatus) AS s_count, 
                       COUNT(ststatus) / SUM(COUNT(ststatus)) over () * 100 AS s_pct 
                  FROM subtasks
                 WHERE user_id=%s
                 GROUP BY ststatus) s
     LEFT JOIN (SELECT pstatus, COUNT(pstatus) AS p_count,
                       COUNT(pstatus) / SUM(COUNT(pstatus)) over () * 100 AS p_pct
                  FROM projects
                 WHERE user_id=%s
                 GROUP BY pstatus) p
            ON p.pstatus = s.ststatus) stats
ORDER BY p_count DESC, s_count DESC
"""

stm_last_comments = """
SELECT cm.stid, st.stname, cm.comment, cm.last_modified_time, cm.cmid, pj.pname, pj.pid
  FROM comments cm
  JOIN (SELECT stname, stid, pid
          FROM subtasks) st
    ON st.stid = cm.stid
  JOIN (SELECT pname, pid
          FROM projects) pj
    ON pj.pid = st.pid
 WHERE user_id = %s
 ORDER BY cm.last_modified_time DESC
 LIMIT %s
"""

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

# build main.css with other css files
def build_stylesheet():
    """
    Consolidate all .css stylesheets into a single one.
    """
    spath = 'static/'
    fnames = [fn for fn in listdir('static') if fn.endswith('.css') and fn != 'main.css']
    css = ''
    for fn in fnames:
        with open(spath+fn, 'r') as f:
            stylesheet = f.read()
            css += stylesheet + '\n'
    with open(spath + 'main.css','w') as f:
        f.write(css)

# return the certificate, key pair for https
def get_ssl():
    """
    Returns the locations of the server's public certificate and private key for https.
    Is consumed by app.run(ssl_context=<output of this f()>)
    """
    cert_dir = '/certs/'
    pub_crt = cert_dir + 'pub/server_crt.pem'
    priv_key = cert_dir + 'private/server_key.pem'
    ssl_context = (pub_crt, priv_key)
    return ssl_context

# send a file for download
def download(loc):
    """
    Returns a file for download from the server.
    """
    return send_file(loc, as_attachment=True)
