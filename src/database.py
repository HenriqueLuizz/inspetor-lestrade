import json
import re
import sys
# from conductor import Conductor

def getIniConns(path):
    list_conn = []
    with open(path, "r+") as ini:
        file_ini = ini.read()
        
        filtro = file_ini.splitlines()
        for line_ini in filtro:
            if line_ini.startswith('REMOTE_SERVER') :
                temp = line_ini.split('=')
                list_conn.append(temp[1].strip().replace(" ",":"))

    return list_conn


def getDbAppserver():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data['appserver']


def getDbPath():
    with open('config.json') as json_file:
        
        data = json.load(json_file)
        
        if not data['broker'].endswith('/'):
            bar = '/'
            if sys.platform.startswith('win32'):
                bar = '\\'
            data['broker'] = data['broker'] + bar

        return data['broker']


def getDbConns():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data['conns']

def getDbConnsUp():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data['alwaysup']


def getDbConnsDown():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data['alwaysdown']

def getDbTurnon():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data['turnon']


def getDbTurnoff():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data['turnoff']

def getDbRecorence():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data['recorence']

def getConfig():
    with open('config.json') as json_file:
        return json.load(json_file)

        
def createTask(self, data):
    dados = data
    
    with open('config.json', 'w') as json_file:
        json.dump(dados, json_file, indent=4)
    with open('config.json') as json_file:
        data = json.load(json_file)
        temp = data #['emp_details']
        # python object to be appended 
        y = { "datetime": "2020-05-10 19:00:00",
            "task": "call",
            "protheus": "/tmp/"
            }
        
        # appending data to emp_details
        temp.append(y)


def listTasks(self):
    with open('config.json', 'r') as json_file:
        dados = json.load(json_file)
        print(dados)


def main(self):
    f = open('config.json','w+')
    for i in range(10):
        f.write('This is line %d\r\n' % (i+1))
    
    f.close
