from flask_script import Manager
from apps import app
from apps.models import db

from flask_migrate import Migrate,MigrateCommand
# from apps.models import User

manager=Manager(app)
Migrate(app,db)

manager.add_command("app",MigrateCommand)

if __name__ == '__main__':
    manager.run()