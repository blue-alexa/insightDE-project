from flask_script import Manager
from edgar_UI import create_app

app = create_app('edgar_UI.config.DevConfig')

manager = Manager(app)


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app)


if __name__ == "__main__":
    manager.run()