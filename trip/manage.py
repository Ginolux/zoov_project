import os
import sys

from flask_script import Manager, Server

from application import create_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



app = create_app()
manager = Manager(app)

manager.add_command('runserver', Server(
    use_debugger = True,
    use_reloader = True,
    host=os.getenv('IP', 'localhost'),
    port = int(os.getenv('PORT', 8082))
))


if __name__ == "__main__":
    manager.run()

