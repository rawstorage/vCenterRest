# The MIT License (MIT)
# Copyright (c) 2016 Dell Inc. or its subsidiaries.

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

try:
    import ConfigParser as Config
except ImportError:
    import configparser as Config
import logging.config
from PyVCR.rest_requests import RestRequests
import time
import csv
import json
# register configuration file
LOG = logging.getLogger('PyVCR')
CONF_FILE = 'PyVCR.conf'
logging.config.fileConfig(CONF_FILE)
CFG = Config.ConfigParser()
CFG.read(CONF_FILE)

# HTTP constants
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'


class rest_functions:
    def __init__(self, username=None, password=None, server_ip=None,
                 verify=False, cert=None):

        if not username:
            username = CFG.get('setup', 'username')
        if not password:
            password = CFG.get('setup', 'password')
        if not server_ip:
            server_ip = CFG.get('setup', 'server_ip')
        if not verify:
            verify = CFG.getboolean('setup', 'verify')
        if not cert:
            cert = CFG.get('setup', 'cert')
        base_url = 'https://%s/rest/' % (server_ip)
        self.rest_client = RestRequests(username, password, verify,
                                        cert, base_url)


    def close_session(self):
        """Close the current rest session
        """
        self.rest_client.close_session()

    ###############################
    # Utility functions
    ###############################

    def create_list_from_file(self,file_name):
        """Given a file, create a list from its contents.  

        :param file_name: the path to the file
        :return: list of contents
        """
        with open(file_name) as f:
            list_item = f.readlines()
        raw_list = map(lambda s: s.strip(), list_item)
        return list(raw_list)

    def read_csv_values(self, file_name):
        '''
        reads any csv file with headers
        You can extract the multiple lists from the headers in the CSV file in your own script call this function and 
        assign to data variable, then extract the lists to the variables example below
        data=ru.read_csv_values(mycsv.csv)
        sgnamelist = data['sgname']
        policylist = data['policy']

        :param file_name CSV file
        :return: Dictionary of data parsed from CSV
        '''
        # open the file in universal line ending mode
        with open(file_name, 'rU') as infile:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile)
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]
        return data

    ###############################
    # system functions USE https://code.vmware.com/apis/62/vcenter-management API explorer to find more endpoints
    ###############################

    def get_all_vm(self):
        """Generates a list of all VMs
        :param No Parameters required
        :return: dict, status_code
        """
        target_uri = "/vcenter/vm"
        return self.rest_client.rest_request(target_uri, GET)

    def set_session(self):
        '''
        Run this function first and include in all scripts, will generate a session
        :return: 
        '''
        target_uri ="/com/vmware/cis/session"

        return self.rest_client.rest_request(target_uri,POST)

    def get_hosts(self):
        '''
        Get a list of all hosts in vCenter
        :return: 
        '''
        target_uri = "/vcenter/host"

        return self.rest_client.rest_request(target_uri, GET)
    def get_cluster(self):
        '''
        Get a list of all clusters in vCenter
        :return: 
        '''
        target_uri = "/vcenter/cluster"

        return self.rest_client.rest_request(target_uri, GET)

    def get_cluster_config(self, cluster_id):
        '''

        :param cluster_id: 
        :return: 
        '''
        target_uri = "/vcenter/cluster/%s" % (cluster_id)

        return self.rest_client.rest_request(target_uri, GET)

    def get_datastores(self):
        '''
        Get a list of all Datastores in vCenter
        :return: 
        '''
        target_uri = "/vcenter/datastore"

        return self.rest_client.rest_request(target_uri, GET)

    def get_datastore_config(self,datastore):
        '''
        
        :param datastore: 
        :return: 
        '''
        target_uri = "/vcenter/datastore/%s" %(datastore)

        return self.rest_client.rest_request(target_uri, GET)

    def get_network(self):
        '''
        Get a list of all hosts in vCenter
        :return: 
        '''
        target_uri = "/vcenter/network"

        return self.rest_client.rest_request(target_uri, GET)

