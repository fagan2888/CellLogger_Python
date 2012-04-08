
import webapp2

import setting

import station
import record
import upload


routes = [
    webapp2.Route(r'/station', handler=station.StationHandler, name='station'),
    webapp2.Route(r'/record' , handler=record.RecordHandler, name='record'),
    webapp2.Route(r'/upload' , handler=upload.UploadHandler, name='upload'),
]

config = {
    'setting' : setting,
}

app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)

