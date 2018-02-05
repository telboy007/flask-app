#!/usr/bin/env python

""" 
    Build your own story web app.

    Database fields:
        Key - matches against the url parameter key to ensure
              correct non-linked text is rendered.
        Parent - tracks where entry originated from
        Pos - tracks which form entry originated from
        Text - text entered into form textbox

"""

import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# app setup
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask_app.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASK_APP_SETTINGS', silent=True)


#key to track position in story
master_key = 'a'


# database functions
def connect_db():
    """ 
        Connects to the specific database. 

        Returns: database connection
    """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """ Initialise new database with single table and starter for 10. """
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.execute('INSERT INTO entries VALUES ("a", "a", "", "In a galaxy far far away...")')
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """ Initializes the database. """
    init_db()
    print('Initialized the database.')


def get_db():
    """ 
        Checks for connection and gets database.

        Returns: database
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """ Closes the database. """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


#app functions
@app.route('/')
def redirect_to_start():
    """ 
        Redirect to ensure key param is in url.

        Returns: redirect command to browser
    """
    global master_key
    return redirect('/key=' + master_key)


@app.route('/key=<key>')
def show_entries(key):
    """ 
        Main function that tracks position in story.

        Args: key - used to track progress in story
        Returns: rendered template to browser
    """
    global master_key
    session['key'] = key
    master_key = key
    db = get_db()
    cur = db.execute('SELECT * FROM entries')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    """ Adds new entries to database with values described in main script docstring.

        Returns: redirect to show_entries to update rendered template
    """
    global master_key
    db = get_db()
    if request.form['text'].strip(' \t\n\r') != "":
        db.execute(
            'insert into entries (key, parent, pos, text) values (?, ?, ?, ?)',
            [str(master_key + request.form['pos']), master_key, request.form['pos'], request.form['text']]
            )
        db.commit()
    else:
        app.logger.info('Empty text field, entry not added.') 
    return redirect(url_for('show_entries', key=master_key))


@app.route('/restart')
def restart_story():
    """ 
        Restarts story by inits DB and redirecting to start
    """
    global master_key
    session['key'] = 'a'
    master_key = 'a'
    init_db()
    return redirect(url_for('show_entries', key=master_key))


if __name__ == '__main__':
    """ Alternative method to run flask app on different port if required. """
    app.run(debug=True, port=8800)