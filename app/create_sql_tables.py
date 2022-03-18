from os import getenv
from time import sleep
import mysql.connector as mysql
import logging
logging.basicConfig(level='INFO')


def init_tables():
    """
    Creates the initial MySQL tables needed for the project tracker to work. 
    Runs every time the container is started, does not affect existing data.
    """
    sdir = 'sql/'
    fnames = [
        'create_accounts_table.sql',
        'create_comments_table.sql',
        'create_projects_table.sql',
        'create_subtasks_table.sql'
    ]
    for f in fnames:
        with open(sdir + f) as sql:
            stm = sql.read()
        cur.execute(stm)
        # don't remember if you need to commit when adding new tables?
        # con.connection.commit()
        logging.info('created table using command:\n{}'.format(stm))



if __name__ == '__main__':
    # sql client inputs
    # get these from the ENV
    host = getenv('MYSQL_HOST') # 'localhost'
    user = getenv('MYSQL_USER') # 'db_user'
    pw = getenv('MYSQL_PASSWORD') # 'db_password123'
    db = getenv('MYSQL_DATABASE') # 'project_tracker'
    attempts = 0
    limit = 15


    # get a connection to the database 
    while (attempts < limit):
        try:
            logging.info('Connecting to the database')
            con = mysql.connect(host=host,user=user, password=pw, database=db)
            cur = con.cursor()

            # create the tables if they don't exist
            init_tables()
            break
        except Exception as e:
            logging.info('encountered an error: {}'.format(e))
            logging.info('trying again in 5 seconds. This is attempt {}/10'.format(attempts+1))
            attempts += 1
            sleep(5)
            if attempts == limit - 1:
                exit('There was an issue connecting to the server and creating tables.' + \
                        ' Try running the container again if this is the first time starting the mysql server')
            continue
