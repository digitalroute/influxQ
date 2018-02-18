#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#    Copyright © 2018 hamid <hamid.noroozi@digitalroute.com>
#
#    Distributed under terms of the GPLv3 license.
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This tool will help you to query an influx database.
"""

from influxdb import InfluxDBClient
import os
import cmd
import configparser

class influxQ(cmd.Cmd):
    prompt = '[influxQ]> '

    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.user_config_dir = os.path.expanduser("~") + "/.config/influxQ"
        self.user_config = self.user_config_dir + "/influxQ.ini"
        self.HOSTNAME = ''
        self.PORT = ''
        self.USER = ''
        self.PASS = ''
        self.DB = ''
        if not os.path.isfile(self.user_config):
            os.makedirs(self.user_config_dir, exist_ok=True)
            self.do_config('')
        else:
            self.config.read(self.user_config)
            self.HOSTNAME = self.config.get('DEFAULT', 'HOSTNAME', fallback='')
            self.PORT = self.config.get('DEFAULT', 'PORT', fallback='')
            self.USER = self.config.get('DEFAULT', 'USER', fallback='')
            self.PASS = self.config.get('DEFAULT', 'PASS', fallback='')
            self.DB = self.config.get('DEFAULT', 'DB', fallback='')
            try:
                self.client = InfluxDBClient(self.HOSTNAME, int(self.PORT), self.USER, self.PASS, self.DB)
            except Exception as e:
                print('Error in configuration.')
                print(e)
                print('Run \'config\' once again')

    def emptyline(self):
        pass

    def do_config(self, line):
        'Configure a connection towards your influxDB instance.'
        self.config['DEFAULT'] = {}
        _hostname = input('Hostname(' + self.HOSTNAME + '): ')
        if not _hostname == '':
            self.HOSTNAME = _hostname
        self.config['DEFAULT']['HOSTNAME'] = self.HOSTNAME
        _port = input('Port(' + self.PORT + '): ')
        if not _port == '':
            self.PORT = _port
        self.config['DEFAULT']['PORT'] = self.PORT
        _user = input('Username(' + self.USER + '): ')
        if not _user == '':
            self.USER = _user
        self.config['DEFAULT']['USER'] = self.USER
        _pass = input('Password(' + self.PASS + '): ')
        if not _pass == '':
            self.PASS = _pass
        self.config['DEFAULT']['PASS'] = self.PASS
        _db = input('Database(' + self.DB + '): ')
        if not _db == '':
            self.DB = _db
        self.config['DEFAULT']['DB'] = self.DB
        with open(self.user_config, 'w') as config_file:
            self.config.write(config_file)
        try:
            self.client = InfluxDBClient(self.HOSTNAME, int(self.PORT), self.USER, self.PASS, self.DB)
        except Exception as e:
            print('Error in configuration.')
            print(e)
            print('Run \'config\' once again')

    def do_quit(self, line):
        'Quit from the tool.'
        return True

    def do_status(self, line):
        'Show the status of the configured influxDB instance.'
        try:
            self.client.ping()
            print('Connection successful.')
        except Exception as e:
            print('Error: Cannot connect to ' + self.DB + ' @ ' + self.HOSTNAME + ':' + str(self.PORT) + ' with ' + self.USER + '/' + self.PASS)

    def default(self, line):
        if not line.endswith(';'):
            line = line + ';'
        try:
            result = self.client.query(line)
            print(result)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    influxQ().cmdloop()
