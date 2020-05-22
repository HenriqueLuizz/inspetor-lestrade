import time
import logging
from string import Template
import database
#from database import getDbPath, getDbConns, getIniConns, getDbAppserver, 

class Conductor:

    def __init__(self, path: str, conns: list, turnon: str, turnoff: str, recorence: str):
        self.path = path
        self.conns = conns
        self.turnon = turnon
        self.turnoff = turnoff
        self.recorence = recorence


    def getPath(self):
        return self.path


    def setPath(self, path):
        self.path = path        


    def setDbPath(self):
        #Verificar se tem o path no arquivo JSON
        self.path = database.getDbPath()


    def getConns(self):
        return self.conns


    def setIniConns(self):
        path = database.getDbPath() + database.getDbAppserver()
        self.conns = database.getIniConns(path)


    def setDbConns(self):
        #Verificar se tem as connexoes no arquivo JSON
        self.conns = database.getDbConns()


    def setConns(self, conns: list):
        self.conns = conns        


    def getTurnon(self):
        return self.turnon


    def setTurnon(self, turnon=''):
        if turnon == '':
            self.turnon = database.getDbTurnon()
        else:    
            self.turnon = turnon

    def getTurnoff(self):
        return self.turnoff

    def setTurnoff(self, turnoff=''):
        if turnoff == '':
            self.turnoff = database.getDbTurnoff()
        else:
            self.turnoff = turnoff

    def getRecorence(self):
        return self.recorence

    def setRecorence(self, recorence=''):
        if recorence == '':
            self.recorence = database.getDbRecorence()
        else:
            self.recorence = recorence


    """Function Writerows
    Responsável por contar as linhas do arquivo .TOTVS_BROKER_COMMAND conforme o conteudo do appserver.ini do Broker Protheus

    """
    def writerows(self, action: str, appconns: list):
        
        row = Template('$action server $conn \n')
        rowsbrokerfile = ""
        poolup = []
        pooldown = []

        if action == 'disable':
            if len(database.getDbConnsUp()) > 0:
                poolup = database.getDbConnsUp()

            for appconn in appconns:
                if not appconn in poolup:
                    rowsbrokerfile += row.substitute(action=action ,conn=appconn)
        else:
            if len(database.getDbConnsDown()) > 0:
                pooldown = database.getDbConnsDown()

            for appconn in appconns:
                if not appconn in pooldown:
                    rowsbrokerfile += row.substitute(action=action ,conn=appconn)

        return rowsbrokerfile

    """Function Broker
    Function responsavel por criar o arquivo de enabe ou disable no diretorio do Broker do Protheus

    O diretório deve ser configurado no arquivo de configuração settings.json ou através do proprio CLI
    que vai gravar o caminho no arquivo settings.json
    """
    def broker(self, action: str, path: str, conns: list):

        print(path + '.TOTVS_BROKER_COMMAND')

        # Limpar lista de conexoes, de acordo com o lista que foi configurada no settings.json (alwaysup ou alwaysdown)
        with open(path + '/.TOTVS_BROKER_COMMAND', 'w') as broker_file:
            if action == 'enable':
                """Cria o arquivo enable no diretório do appserver."""
                broker_file.write(self.writerows('enable',conns))
                pass
            elif action == 'disable':
                """Cria o arquivo disable no diretório do appserver."""
                broker_file.write(self.writerows('disable',conns))
                pass
            else:
                """Opção invalida"""
                pass


    def enableBroker(self):
        print('Enable - ' + time.ctime())
        self.broker('enable', self.getPath(), self.getConns())


    def disableBroker(self):
        print('Disable - ' + time.ctime())
        self.broker('disable', self.getPath(), self.getConns())
