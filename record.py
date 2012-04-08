
import logging
import urllib
import os
import sys
import datetime
import json

from google.appengine.ext import db
from google.appengine.api import users
import webapp2
import jinja2

import model

tpl_path = os.path.join(os.path.dirname(__file__), 'tpl')
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(tpl_path))

def filter_localtime(value, format='%Y-%m-%d %H:%M:%S'):
    # convert to CST
    value = value - datetime.timedelta(hours=-8)
    return value.strftime(format)

jinja_environment.filters['localtime'] = filter_localtime

logging.debug('load station data')
station_data = json.load(open(os.path.join(os.path.dirname(__file__)
    , 'data/station.json')))

station_name_cache = {}
def filter_station_name(value):
    key = str(value)
    if key in station_name_cache:
        logging.debug('hit %s' % (key,))
        return station_name_cache[key]

    for line in station_data['stations']:
        for station in line['station']:
            if station['id'] == value :
                result = '%s %s' % (line['line'], station['name'])
                station_name_cache[key] = result
                return result

    return 'unknown'

jinja_environment.filters['station_name'] = filter_station_name

class RecordHandler(webapp2.RequestHandler):

    def output(self, tpl, vars):
        """ 
        output with template and variables 
        """
        self.response.content_type = 'text/html'
        template = jinja_environment.get_template('%s.html' % tpl)
        self.response.out.write(template.render(vars))

    def action_delete(self):
        items = self.request.POST.getall('checkitem')

        if len(items) == 0 :
            return 'no record checked, cancel'

        count = 0
        for key in items:
            record = model.Record.get(key)
            if(record):
                db.delete(record) 
                count += 1

        return 'deleted %d record' % (count, )

    def action_approve(self):
        items = self.request.POST.getall('checkitem')

        if len(items) == 0 :
            return 'no record checked, cancel'

        count = 0
        for key in items:
            record = model.Record.get(key)
            if(record):

                cell = model.Cell(record.lac, record.cid)

                station = model.Station.get_or_insert_station(str(record.station))
                station.cell.add(cell)
                station.put()

                record.approved = True
                count += 1
                record.put()

        return 'approved %d record' % (count, )

    def action_decline(self):
        items = self.request.POST.getall('checkitem')

        if len(items) == 0 :
            return 'no record checked, cancel'

        count = 0
        for key in items:
            record = model.Record.get(key)
            if(record):
                record.approved = False
                count += 1
                record.put()

        return 'declined %d record' % (count, )

    def post(self):

        msg = ''
        action = self.request.get('action')
        if action == 'delete' :
            msg = self.action_delete()
        elif action == 'approve' :
            msg = self.action_approve()
        elif action == 'decline' :
            msg = self.action_decline()
        else:
            msg = 'invalid action'

        offset = self.request.get('offset')

        vars = {}
        vars['status'] = msg
        vars['next']   = self.uri_for('record', offset=offset)
        vars['autojump'] = '1'
        self.output('op', vars)


    def get(self):

        offset = int(self.request.get('offset', default_value='0'))
        limit = 30
        sql = "SELECT * FROM Record ORDER BY time DESC LIMIT %d, %d" % (offset, limit+1)
        logging.debug(sql)

        res = db.GqlQuery(sql)
        records = list(res)

        logging.debug(len(records))

        pager = {}
        pager['offset'] = offset
        if offset > 0 :
            pager['prev'] = offset - limit
        if len(records) == limit + 1 :
            pager['next'] = offset + limit
        logging.debug(pager)



        vars = {}
        vars['pager'] = pager
        vars['records'] = records[:limit]
        vars['action_url'] = self.uri_for('record', offset=offset)
        self.output('record', vars)



