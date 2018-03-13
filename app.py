from flask import flash, request, redirect, url_for, abort
from flask import render_template
from flask.ext.login import login_required, login_user, logout_user
from app_factory import app, db, login_manager
from models import *
from forms import LoginForm, RegistrationForm
from json import dumps, loads
import google_books_service
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.before_request
def before_request():
    """Connect to the database before each request."""
    # g = global object Flask uses for passing information to views/modules.
    # g.db = db
    # g.db.connect()
    pass


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    # g.db.close()
    return response


@app.route('/')
def home(name="default", test="default"):
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        add_to_database(user)
        login_user(user, remember=True)
        flash('Welcome!', category='success')
        return redirect(url_for('app_default'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_email(form.email.data)
        login_user(user, remember=True)

        next = request.args.get('next')
        # WE ARE CURRRENTLY ASSUMING 'next' IS VALID. IF PERMISSIONS ARE ADDED
        # LATER, THEN WE SHOULD ADD ADDITIONAL VALIDATION

        return redirect(next or url_for('app_default'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(message=u'You have logged out. Hope to see you soon!',
          category='success')
    return render_template('index.html')


@app.route('/app', methods=['GET', 'POST'])
@login_required
def app_default():
    return render_template('app.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    pass # TODO allow user to get or modify their settings.


### BOOKS ###

@app.route('/books/add', methods=['GET'])
def add_book():
    query = request.args.get("query")
    books = []
    if query:
        books = google_books_service.search_books(query)
    return render_template('books/add.html', books=books)

### HOUSES ###

@app.route('/houses/<house_id>', methods=['GET'])
def house(house_id):
    house = House.get_house_by_id(house_id)
    house_books = house.get_all_books()
    return render_template('houses/id.html', books=house_books)

@app.route('/houses/<house_id>/members', methods=['GET'])
def house_members(house_id):
    house = House.get_house_by_id(house_id)
    house_members = house.members
    return render_template('houses/members.html', members=house_members)

app.route('/houses/add', methods=['GET', 'POST'])
def add_house(house_id):
    pass # TODO logic for creating a new house
    # return render_template('houses/add.html', house=house)

### USERS ###

@app.route('/users/<user_id>', methods=['GET'])
def user(user_id):
    user = User.get_user_by_id(user_id)
    return render_template('users/id.html', user=user)

@app.route('/users/book_copies/<book_copy_id>', methods=['GET'])
def user_book_copy(book_copy_id):
    pass 
    # TODO:
    #   Add a unique primary key for user_books table. 
    #   Get a user_book entry by id, and return it.
    # return render_template('users/book_copy_id.html', book=book)


### HANDLERS ###

@login_manager.user_loader
def load_user(userid):
    return User.get_user_by_id(userid)


@login_manager.unauthorized_handler
def unauthorized():
   flash(message='You must be logged in to do that!', category='error')
   return 200


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


# # COMMENT THIS CODE OUT FOR PRODUCTION, OR DON'T DISPLAY THE ERROR
# @app.errorhandler(500)
# def page_not_found(error):
#     return render_template('internal_server_error.html', error=error), 500


def add_to_database(object):
    db.session.add(object)
    db.session.commit()


if __name__ == '__main__':
    print("DATABASE_URL: " + app.config['SQLALCHEMY_DATABASE_URI'])
    print("DEBUG: " + str(app.config['DEBUG']))
    app.run()
"""
When the Python interpreter reads a source file, it executes all of the code
found in it. Before executing the code, it will define a few special
variables. For example, if the python interpreter is running that module
(the source file) as the main program, it sets the special __name__ variable
to have a value "__main__". If this file is being imported from another
module, __name__ will be set to the module's name.

In the case of your script, let's assume that it's executing as the main
function, e.g. you said something like

python threading_example.py

on the command line. After setting up the special variables, it will execute
the import statement and load those modules. It will then evaluate the def
block, creating a function object and creating a variable called myfunction
that points to the function object. It will then read the if statement and
see that __name__ does equal "__main__", so it will execute the block shown
there.

One of the reasons for doing this is that sometimes you write a module
(a .py file) where it can be executed directly. Alternatively, it can also be
imported and used in another module. By doing the main check, you can have
that code only execute when you want to run the module as a program and not
have it execute when someone just wants to import your module and call your
functions themselves.
http://stackoverflow.com/questions/419163/what-does-if-name-main-do
"""
