import os
from flask import Flask
from . import db
from . import auth
from . import blog

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY = b'\xd0\xddL\x98\xb4\xec8\x0b\x7f!t\xb1X\xb1\xc9\xca',
    DATABASE = os.path.join(app.instance_path, 'db.sqlite3')
  )

  if test_config is None:
    # load the instance config, if it exist, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # a simple page that says hello
  @app.route('/hello/')
  def hello():
    return 'Hello, World!'

  # create database
  db.init_app(app)

  app.register_blueprint(auth.bp)

  app.register_blueprint(blog.bp)
  app.add_url_rule('/', endpoint='index')

  return app