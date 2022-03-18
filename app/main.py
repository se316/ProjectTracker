from flask import Flask, render_template, request, redirect, url_for, session
from routes import view, delete, edit, new
from extensions import mysql as con
from os import getenv

# configure the app for MySQL
app = Flask(__name__)
app.secret_key = 'foobar'
# get these from the environment
app.config['MYSQL_HOST'] = getenv('MYSQL_HOST') # localhost
app.config['MYSQL_USER'] = getenv('MYSQL_USER') # 'db_user'
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD') # 'db_password123'
app.config['MYSQL_DB'] = getenv('MYSQL_DATABASE') # 'project_tracker'

# initialize the shared "connection" object
con.init_app(app)

# register blueprints
app.register_blueprint(view.view_bp)
app.register_blueprint(delete.delete_bp)
app.register_blueprint(edit.update_bp)
app.register_blueprint(new.new_bp)

# no url args should take you home or to the login page depending on whether
# ur logged in or not
@app.route('/')
def index():
    return redirect(url_for('view.home'))

# run the server
app.run(debug=True, host='0.0.0.0', port='8080')
