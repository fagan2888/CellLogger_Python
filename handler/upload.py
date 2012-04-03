
import json
import datetime
import logging
import sys

import webapp2

import dao.record



E = {
    'INPUT_JSON'      : 1,
    'INPUT_FORMAT'    : 2,
    'EMPTY_CLIENT'    : 3,
    'INVALID_REQUEST' : 5,
}

class UploadHandler(webapp2.RequestHandler):

    def error(self, errno, description=None):
        self.output(errno, description)

    def ok(self, data):
        self.output(0, data)

    def output(self, errno, data):
        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps({
            'error':errno, 
            'payload':{
                'description':data,
            },
        }, sort_keys=True, indent=4))

    def get(self):
        self.error(E['INVALID_REQUEST'], None)

    def post(self):

        try:
            data = json.loads(self.request.body)
        except (ValueError, TypeError) as (e,):
            self.error(E['INPUT_JSON'], e)
            return 

        try:
            client = data['client']
            records = data['records']
        except KeyError as (e,) :
            self.error(E['INPUT_FORMAT'], e)
            return 

        if not client:
            self.error(E['EMPTY_CLIENT'])
            return

        statusCount = {'success':0, 'failed':0}

        for re in records:
            one = dao.record.Record()

            try :
                one.client = client
                one.client_id = str(re['id'])
                one.network_type = re['network_type']
                one.lac = re['lac']
                one.cid = re['cid']
                one.station = re['station']
                one.signal = re['signal']
                one.client_time = datetime.datetime.fromtimestamp(re['time'])
                one.time = datetime.datetime.now()
                one.approved = False

                one.put()
                statusCount['success'] += 1
            except :
                e = repr(sys.exc_info())
                logging.warning('put failed: %s' % (e,))
                statusCount['failed'] += 1
                

        self.ok(statusCount)
        return
