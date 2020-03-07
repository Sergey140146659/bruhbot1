from config import DB as db
from models import *

db.connect()
db.create_tables([User, Message])
db.close()