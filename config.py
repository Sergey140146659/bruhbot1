from decouple import config
from playhouse.db_url import connect

TOKEN = config("TOKEN")
PORT = config("PORT", default=8443, cast=int)
HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
DB = connect(config("DB_URL", default="sqlite:///bot.db"))

