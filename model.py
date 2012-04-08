
import json
import datetime
import logging

from google.appengine.ext import db

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cell):
            return {'lac':obj.lac, 'cid':obj.cid}
        return json.JSONEncoder.default(self, obj)
        
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

class Cell(object):

    def __init__(self, lac, cid):
        self.lac = lac
        self.cid = cid

    def __str__(self):
        return '%s,%s' % (self.lac, self.cid)

    def __eq__(self, obj):
        return ( self.lac == obj.lac and self.cid == obj.cid )

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash(self.__str__())

    def __dict__(self):
        return {'lac':self.lac, 'cid':self.cid};

class StationCellProperty(db.Property):

    data_type = list

    # For writing to datastore.
    def get_value_for_datastore(self, model_instance):
        cells = super(StationCellProperty,
            self).get_value_for_datastore(model_instance)

        value = list(cells)

        if cells is not None:
            return db.Text(json.dumps(value, cls=ModelEncoder))
        else:
            return db.Text("[]")


    # For reading from datastore.
    def make_value_from_datastore(self, value):
        value=super(StationCellProperty, self).make_value_from_datastore(value)

        if value is None:
            return []
        
        jcells = json.loads(str(value))

        cells = []
        for c in jcells:
            cell = Cell(c['lac'], c['cid'])
            cells.append(cell)
        
        return set(cells)

    def validate(self, value):
        logging.debug('validate %s', repr(value))
        if value is not None and not isinstance(value, set):
            raise BadValueError('Property %s must be a set '
                                '(%s)' %
                                (self.name, value))
        return super(StationCellProperty, self).validate(value)

    def empty(self, value):
        return not value


class Station(db.Model):

    station  = db.StringProperty(required=True)
    cell     = StationCellProperty()
    time     = db.DateTimeProperty()

    @staticmethod
    def get_or_insert_station(station):
        kwargs={}
        kwargs['station'] = station
        kwargs['time'] = datetime.datetime.now()
        kwargs['cell'] = set([])
        
        return Station.get_or_insert(station, **kwargs)

