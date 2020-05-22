import json
import re
import sys
import common
# from conductor import Conductor


##########################################################################################
"""Verifica o arquivo appserver.ini do broker Protheus
    Retorna todos os ips e portas dos appservers configurados no Broker

    :return List connection
"""
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

##########################################################################################
"""Acessa o arquivo settings.json para localizar o nome do arquivo ini do Broker

    :return Str
"""
def getDbAppserver():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'appserver' in data:
            return data['appserver']
        else:
            return

"""Acessa o arquivo settings.json para localizar o caminho appserver Broker

    :return Str
"""
def getDbPath():
    with open('settings.json') as json_file:
        
        data = json.load(json_file)

        if 'broker' in data:
            if not data['broker'].endswith('/'):
                bar = '/'
                if sys.platform.startswith('win32'):
                    bar = '\\'
                data['broker'] = data['broker'] + bar

            return data['broker']
        else:
            return

"""Acessa o arquivo settings.json para localizar as conexões do de ip e porta dos appserver
    Essa função é superior getIniConns(), porque nesta chave só tera as conexões que o usuário 
    deseja controlar pelo CLI

    :return List connections
"""
def getDbConns():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'conns' in data:
            return data['conns']
        else:
            return

"""Acessa o arquivo settings.json para localizar as conexões que não podem ser desativadas ou desligadas

    :return Str
"""
def getDbConnsUp():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'alwaysup' in data:
            return data['alwaysup']
        else:
            return

"""Acessa o arquivo settings.json para localizar as conexões que podem ser desativadas ou desligadas

    :return Str
"""
def getDbConnsDown():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'alwaysdown' in data:
            return data['alwaysdown']
        else:
            return

"""Acessa o arquivo settings.json para localizar o horarios que deve ativar as conexões

    :return Str
"""
def getDbTurnon():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'turnon' in data:
            return data['turnon']
        else:
            return

"""Acessa o arquivo settings.json para localizar o horarios que deve desativar as conexões

    :return Str
"""
def getDbTurnoff():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'turnoff' in data:
            return data['turnoff']
        else:
            return
            
"""Acessa o arquivo settings.json para localizar o tipo de recorrencia

    :return Str
"""
def getDbRecorence():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'recorence' in data:
            return data['recorence']
        else:
            return

"""Verifica qual é o nome da cloud configurada

    :return list[Str] 
"""
def getCloud():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        for cloud in ['oci','aws','azure','gcp']:
            if cloud in data:
                return [cloud]


def getOci():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'oci' in data:
            return data['oci']
        else:
            return []

def getAWS():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'aws' in data:
            return data['aws']
        else:
            return []

def getAzure():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'azure' in data:
            return data['azure']
        else:
            return []

def getGcp():
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if 'gcp' in data:
            return data['gcp']
        else:
            return []

"""Acessa o arquivo settings.json para localizar todas as chaves configuradas

    :return Str
"""
def getConfig():
    with open('settings.json') as json_file:
        return json.load(json_file)

#####################################################################################


def createTask(self, data):
    dados = data
    
    with open('settings.json', 'w') as json_file:
        json.dump(dados, json_file, indent=4)
    with open('settings.json') as json_file:
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
    with open('settings.json', 'r') as json_file:
        dados = json.load(json_file)
        print(dados)

def main(self):
    f = open('settings.json','w+')
    for i in range(10):
        f.write('This is line %d\r\n' % (i+1))
    
    f.close
