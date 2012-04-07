
import logging
import urllib
import os
import sys

from google.appengine.ext import db
from google.appengine.api import users
import webapp2
import jinja2

tpl_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tpl')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(tpl_path))

class MainHandler(webapp2.RequestHandler):

    def output(self, tpl, vars):
        """ 
        output with template and variables 
        """
        self.response.content_type = 'text/html'
        template = jinja_environment.get_template('%s.html' % tpl)
        self.response.out.write(template.render(vars))

    def post(self):

        vars = {}
        vars['status'] = '...';
        vars['next']   = '/';
        vars['autojump'] = '1';
        self.output('op', vars)


    def get(self):

        offset = int(self.request.get('offset', default_value='0'))
        limit = 30
        sql = "SELECT * FROM Record ORDER BY time DESC LIMIT %d, %d" % (offset, limit+1)
        logging.debug(sql)

        res = db.GqlQuery(sql)
        records = tuple(res)

        logging.debug(len(records));

        pager = {}
        if offset > 0 :
            pager['prev'] = offset - limit
        if len(records) == limit + 1 :
            pager['next'] = offset + limit
        logging.debug(pager)



        vars = {}
        vars['pager'] = pager
        vars['records'] = records[:limit]
        self.output('record', vars)



