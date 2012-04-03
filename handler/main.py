

from google.appengine.ext import db
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/plain'

        records = db.GqlQuery("SELECT * FROM Record ")
        for r in records:

            self.response.out.write('lac=%s, cid=%s client_time=%s, time=%s\n'
                % (r.lac, r.cid, r.client_time, r.time))


