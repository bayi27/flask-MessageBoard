#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User,Post, Comment
from flask_script import Manager, Shell
#Flask-Script是一个Flask拓展，为Flask程序添加了一个命令行解析器，它自带了一组常用选项，而且还支持自定义命令
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)#初始化flask-script
migrate = Migrate(app, db)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User,Post=Post, Comment=Comment) #打开命令行时默认导入的参数

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()

if __name__ == '__main__':
    manager.run()