import json
import time
import sys
import click
from string import Template
from ipsetup import Setup

class Service:



    def writerows(self, action: str, setup: Setup):
        
        row = Template('$action server $conn \n')
        rowsbrokerfile = ""
        poolup = []
        pooldown = []


        if action == 'disable':
            if len(setup.getAlwaysup()) > 0:
                poolup = setup.getAlwaysup()

            for appconn in setup.getConns():
                if not appconn in poolup:
                    rowsbrokerfile += row.substitute(action=action ,conn=appconn)
        else:
            if len(setup.getAlwaysdown()) > 0:
                pooldown = setup.getAlwaysdown()

            for appconn in setup.getConns():
                if not appconn in pooldown:
                    rowsbrokerfile += row.substitute(action=action ,conn=appconn)

        return rowsbrokerfile


    def broker(self, action: str, setup: Setup):

        path = setup.getAppserverPath()

        if not path.endswith('/') and not path.endswith('\\'):
            bar = '/'
            if sys.platform.startswith('win32'):
                bar = '\\'
            path = path + bar

        print(path + '.TOTVS_BROKER_COMMAND')

        # Limpar lista de conexoes, de acordo com o lista que foi configurada no settings.json (alwaysup ou alwaysdown)
        with open(path + '.TOTVS_BROKER_COMMAND', 'w') as broker_file:
            if action == 'enable':
                """Cria o arquivo enable no diretório do appserver."""
                broker_file.write(self.writerows('enable', setup))
                pass
            elif action == 'disable':
                """Cria o arquivo disable no diretório do appserver."""
                broker_file.write(self.writerows('disable', setup))
                pass
            else:
                """Opção invalida"""
                pass

    
    def enable_auto(self):
        setup = object.__new__(Setup)
        setup.load()

        self.enable_broker(setup)

    def disable_auto(self):
        setup = object.__new__(Setup)
        setup.load()

        self.disable_broker(setup)

    def enable_broker(self, setup: Setup):
        
        print('Enable - ' + time.ctime())
        self.broker('enable', setup)
        
        with open('.protheus', "w") as p_file:
            p_file.write('enabled')


    def disable_broker(self, setup: Setup):
        print('Disable - ' + time.ctime())
        self.broker('disable', setup)

        with open('.protheus', "w") as p_file:
            p_file.write('disabled')



    def info(self, setup: Setup):

        # Mostrar os serviços que estão sendo observado
        allconns = setup.getConns()
        # Lista de Sempre ativo
        alwaysup = setup.getAlwaysup()
        # Lista de Sempre desativo
        alwaysdown = setup.getAlwaysdown()
        # Status dos serviço atual Habilitado ou Desabilitado
        with open('.protheus', "r") as p_file:
            status = p_file.read()

        if len(allconns) > 0:
            click.secho('Serviços que estão sendo observado:', bold=True)
            for conn in allconns:
                click.secho('REMOTE SERVER : ' + click.style(conn, bold=True), bold=False)

        if len(alwaysup) > 0:
            print('')            
            click.secho('Serviços listados para sempre ficar habilitado:', bold=True)
            for up in alwaysup:
                click.secho('REMOTE SERVER : ' + click.style(up, bold=True, fg='cyan'), bold=False)

        if len(alwaysdown) > 0:
            print('')
            click.secho('Serviços listados para sempre ficar desabilitado:', bold=True)            
            for down in alwaysdown:
                click.secho('REMOTE SERVER : ' + click.style(down,bold=True, fg='red'), bold=False)
        
        print('')
        if status == 'enabled':
            click.secho('Os serviços estão ' + click.style('habilitado',bold=True, fg='green') + ' agora.', bold=False)
        elif status == 'disable':
            click.secho('Os serviços estão ' + click.style('desabilitado',bold=True, fg='red') + ' agora.', bold=False)




