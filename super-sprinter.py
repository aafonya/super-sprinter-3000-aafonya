# all the imports
import os
from peewee import *
from flaskr.connectdatabase import ConnectDatabase
from flaskr.models import User_stories
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'super-sprinter.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('SUPER-SPRINTER_SETTINGS', silent=True)


def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([User_stories], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
@app.route('/list')
def show_stories():
    user_stories = User_stories.select().order_by(User_stories.id)
    return render_template('list.html', stories=stories)


@app.route('/form', methods=['GET', 'POST'])
def form():
    story = []
    return render_template('form.html', story=story, header='Create story', button='Create')


@app.route('/story/', methods=['POST'])
def record_story():
    new_record = User_stories.create(title=request.form['title'],
                                     text=request.form['text'],
                                     criteria=request.form['criteria'],
                                     business_value=request.form[
                                         'business_value'],
                                     estimation=request.form['estimation'],
                                     status=request.form['status'])
    new_record.save()
    return redirect(url_for('show_stories'))


@app.route('/story/<story_id>', methods=['GET'])
def edit(story_id):
    story = User_stories.get(User_stories.id == story_id)
    return render_template("form.html", story=story, header="Edit story", button="Update")


@app.route('/story/', methods=['POST'])
def edit_story(story_id):
    edit_record = User_stories.update(title=request.form['title'],
                                      text=request.form['text'],
                                      criteria=request.form['criteria'],
                                      business_value=request.form[
                                          'business_value'],
                                      estimation=request.form['estimation'],
                                      status=request.form['status']).where(Story.id == story_id)
    edit_record.save()
    return redirect(url_for('show_stories'))


@app.route('/delete/<story_id>', methods=['POST'])
def delete_story(story_id):
    story = User_stories.select().where(User_stories.id == story_id).get()
    User_stories.delete_instance()
    return redirect(url_for('show_stories'))

if __name__ == '__main__':
    init_db()
app.run(debug=True)
