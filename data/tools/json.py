import json
import logging
import os

from constants import *
from data.tools.dbtool import DBTool

class JsonDBTool(DBTool):
    HEADER = 'registered_id_actions'
    DEFAULT_DB = 'data/register_id_acts.json'
    def __init__(self, file_name=DEFAULT_DB):
        self._set_file(file_name)

    def register(self, id, command=NO_ACTION, save=True):
        logging.debug('id to register: %s command: %s' % (id, command))
        registered_id = { 'id': id, 'command': command }
        self.data[HEADER][id] = command
        if save:
            self.save()
        return registered_id
    
    def save(self):
        with open(self.file_name, 'w') as outfile:
            json.dump(self.data, outfile)
        logging.info('Registration file updated.')
    
    def get(self, id):
        return self.data[self.HEADER].get(id, {})
    
    def get_all(self):
        devices = []
        for key in self.data.get(self.HEADER):
            devices.append(self.data.get(self.HEADER).get(key))
        return devices

    def load_db(self, file_name=DEFAULT_DB):
        self._set_file(file_name)

    def _set_file(self, file_name=DEFAULT_DB):
        self.file_name = file_name
        if os.path.isfile(self.file_name):
            db_file = open(self.file_name)
            self.data = json.load(db_file)
            header = self.data.get(self.HEADER, None)
            if self.data.get(self.HEADER, None) is None:
                raise Exception('Expected header \'%s\' not found in '
                                'provided dump file!' % (self.HEADER))
        else:
            self.data = { self.HEADER: {} }
            self.save()
            logging.info('%s file not found, creating a new one...' %
                         (self.file_name))
        logging.info('Set registration file to %s' % (self.file_name))

    def _upload_file(self, file_name, save=True):
        if os.path.isfile(file_name):
            upload = open(file_name)
            data = json.load(upload)
            if not self.data.get(HEADER, None):
                raise Exception('Expected header \'%s\' not found in '
                                'provided dump file!' % (HEADER))
            else:
                for key in data:
                    self.data[HEADER][key] = data[HEADER][key]
                if save:
                    self.save()
                
        else:
            # No file found at that location...
            logging.warning('%s file not found! Upload aborted.' % (file_name))

    def upload_to_db(self, file_name, save=True):
        self._upload_file(file_name, save)
