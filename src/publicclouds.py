import json
import subprocess
import database
import common

def identifyCloud():
    return database.getCloud()

def resultOCI(d):
    if d['status']:
        o = json.loads(d['result'])
        
        if 'data' in o:
            name = o['data']['display-name']
            lifecycle = o['data']['lifecycle-state']

            print(f'Conexão realizada com sucesso!\n {name} - {lifecycle}')
            return True

    else:
        print('Falha ao realizar a conexão com o OCI \n' + d['result'])
        return False


def checkOCI():
    for iid in database.getOci():
        command=f'oci compute instance get --instance-id {iid}'
        data = common.run(command)
        if data['status']:
            print('Conexão realizada com sucesso!\n')
            resultOCI(data)
            return True
        else:
            print('Falha ao realizar a conexão com o OCI \n' + data['result'])
            return False
        break
    

def instancieOCI(iids:list, action='get'):
    if action.lower() == 'start':
        
        for iid in iids:
            data = common.run(f'oci compute instance action --instance-id {iid} --action START')
            resultOCI(data)

    elif action.lower() == 'stop':
        
        for iid in iids:
            data = common.run(f'oci compute instance action --instance-id {iid} --action STOP')
            resultOCI(data)
    else:
        
        for iid in iids:
            data = common.run(f'oci compute instance get --instance-id {iid}')
            resultOCI(data)


def oci(action='get'):
    print(f'OCI operation {action} running... ')
    result = database.getOci()   
    instancieOCI(result,action)

