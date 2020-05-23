import json
import os

"""Classe de configuração do CLI INSPETOR PROTHEUS
"""
class Setup:


    def __init__(self, appserver_path, appserver_name, conns, alwaysup, alwaysdown, is_default=False ):
        self.appserver_path = appserver_path
        self.appserver_name = appserver_name
        self.conns = conns
        self.alwaysup = alwaysup
        self.alwaysdown = alwaysdown
        self.is_default = is_default


    def getAppserverPath(self):
        return self.appserver_path


    def setAppserverPath(self, path):
        self.appserver_path = path


    def getAppserverName(self):
        return self.appserver_path


    def setAppserverName(self, name):
        self.appserver_name = name


    def getAlwaysup(self):
        return self.alwaysup


    def setAlwaysup(self, alwaysup):
        self.alwaysup = alwaysup


    def getAlwaysdown(self):
        return self.alwaysdown


    def setAlwaysdown(self, alwaysdown):
        self.alwaysdown = alwaysdown


    def getConns(self):
        return self.conns


    def setConns(self, conns):
        self.conns = conns


    def getIniConns(self):
        list_conn = []
        with open(self.appserver_path + self.appserver_name, "r+") as ini:
            file_ini = ini.read()
        
            filtro = file_ini.splitlines()
            for line_ini in filtro:
                if line_ini.startswith('REMOTE_SERVER') :
                    temp = line_ini.split('=')
                    list_conn.append(temp[1].strip().replace(" ",":"))

        return list_conn            


    def setConfig(self, key, value):
        conf = {}

        with open('settings.json') as json_file:
            conf = json.load(json_file)
            conf.update(dict({key:value}))

        with open('settings.json', 'w') as json_read:
            json.dump(conf, json_read,indent=4)

        return conf

    def getConfig(self):
        conf = {}

        with open('settings.json') as json_file:
            conf = json.load(json_file)
        return conf
        
        
    def init_setup(self):
        init_data = {
            'appserver_path' : os.getcwd(),
            'appserver_name' : 'appserver.ini',
            'conns' : [],
            'alwaysup' : [],
            'alwaysdown' : [],
        }
        with open('settings.json') as json_file:
            conf = json.load(json_file)
            conf.update(init_data)
        
        with open('settings.json', 'w') as json_read:
            json.dump(conf, json_read,indent=4)

        pass


    def load(self):
        data = self.getConfig()
        
        self.appserver_path = data.get('appserver_path','')
        self.appserver_name = data.get('appserver_name','')
        self.conns = data.get('conns',[])
        self.alwaysup = data.get('alwaysup',[])
        self.alwaysdown = data.get('alwaysdown',[])

    def updateConns(self):

        ips = self.getIniConns()
        self.setConns(ips)
        self.setConfig('conns',ips)

        