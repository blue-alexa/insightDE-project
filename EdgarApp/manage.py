from flask_script import Manager
from EdgarApp import create_app

app = create_app('EdgarApp.config.DevConfig')

manager = Manager(app)


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app)


if __name__ == "__main__":
    manager.run()

# python3 manage.py runserver -h 0.0.0.0 -p 5000