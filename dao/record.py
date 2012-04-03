
from google.appengine.ext import db

class Record(db.Model):
    client       = db.StringProperty()
    client_id    = db.StringProperty()
    network_type = db.IntegerProperty()
    lac          = db.IntegerProperty()
    cid          = db.IntegerProperty()
    station      = db.IntegerProperty()
    signal       = db.IntegerProperty()
    client_time  = db.DateTimeProperty()
    time         = db.DateTimeProperty()
    approved     = db.BooleanProperty()


