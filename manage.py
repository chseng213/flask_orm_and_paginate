from flask import Flask
from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from apps import create_app

app = create_app()
manager = Manager(app=app)
manager.add_command('start', Server(port=9000))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
