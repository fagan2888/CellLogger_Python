
import webapp2

import setting

import record
import upload


routes = [
    webapp2.Route(r'/record' , handler=record.RecordHandler, name='record'),
    webapp2.Route(r'/upload' , handler=upload.UploadHandler, name='upload'),
]

config = {
    'setting' : setting,
}

app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)

