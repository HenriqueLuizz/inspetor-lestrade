import argparse
import time
import schedule
import pprint
from datetime import datetime
from conductor import Conductor
from database import getConfig 


def schedEnable(obj:Conductor):
    print(time.ctime())
    print(obj.getTurnon())
    schedule.every().day.at(obj.getTurnon()).do(obj.enableBroker)


def schedDisable(obj:Conductor):
    print(time.ctime())
    print(obj.getTurnoff())
    schedule.every().day.at(obj.getTurnoff()).do(obj.disableBroker)


def enableNow(obj:Conductor):
    obj.enableBroker()


def disableNow(obj:Conductor):
    obj.disableBroker()


def listConfig():
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(getConfig())

def setConfig():

    cond = object.__new__(Conductor)
    cond.setDbPath()

    cond.setIniConns()
    cond.setTurnon()
    cond.setTurnoff()
    cond.setRecorence()

    return cond

def runConfig(cond: Conductor):
    schedEnable(cond)
    schedDisable(cond)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print('Parei com sched')
            break


def main():

    parser = argparse.ArgumentParser(prog='insp-protheus',
                                     usage='%(prog)s [options]',
                                     description='Inspetor Protheus é uma ferramenta para auxiliar na gestão dos serviços',
                                     epilog='%(prog)s está em constante desenvolvimento!')
    parser.add_argument('-v','--version', 
                                help='Exibe a versão do Inspertor Protheus', 
                                action='store_true')
    parser.add_argument('-L','--list', 
                                help='Lista as configurações do arquivo config.json', 
                                action='store_true')
    # parser.add_argument('-i','--install', 
    #                           help='Instala o inspetor como serviço', 
    #                           action='store_false')
    # parser.add_argument('-T','--test-cloud', 
    #                           help='Valida a conexão com o cloud', 
    #                           action='store_false')
    parser.add_argument('-off','--power-off', 
                                help='Desliga as instancias configuradas', 
                                action='store_true')
    parser.add_argument('-on','--power-on', 
                                help='Liga as instancias configuradas', 
                                action='store_true')
    parser.add_argument('-r','--run', 
                                help='Executa os agendamentos configurados em modo console', 
                                action='store_true')
    parser.add_argument('-d','--disable', 
                                help='Desativa todos os serviços configurados agora', 
                                action='store_true')
    parser.add_argument('-e','--enable', 
                                help='Ativa todos os serviços configurados agora', 
                                action='store_true')
    # parser.add_argument('-c','--configure', 
    #                           help='Habilita o mode de configuração',
    #                           action='store_true')
    # parser.add_argument('-C','--check-list', 
    #                           help='Lista os agendamentos configurados', 
    #                           action='store_false')
    # parser.add_argument('-d','--delete', 
    #                           help='Deleta todos os agendamentos', 
    #                           action='store_false')

    args = parser.parse_args()

    if args.version:
        print('Inspetor Protheus - v0.0.1')
    elif args.list:
        print('O arquivo de configuração...')
        listConfig()
    elif args.run:
        print('O arquivo de configuração...')
        runConfig(setConfig())
    elif args.disable:
        print('Será desativado os serviços agora!')
        disableNow(setConfig())
    elif args.enable:
        print('Será ativado os serviços agora!')
        enableNow(setConfig())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
