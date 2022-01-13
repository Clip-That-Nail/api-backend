from os import environ 

SQLALCHEMY_DATABASE_URI = environ.get('DB_URI') # "mysql://username:password@server/db" # TODO: DB config - set MySQL DB config for dev and for production
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True