
import webapp2

import setting
import handler.main
import handler.upload


routes = [
    webapp2.Route(r'/'       , handler=handler.main.MainHandler    , name='home'  ),
    webapp2.Route(r'/upload' , handler=handler.upload.UploadHandler, name='upload'),
]

config = {
    'setting' : setting,
}

app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)
