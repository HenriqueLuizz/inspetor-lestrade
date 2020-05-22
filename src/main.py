import argparse
import time
import schedule
import pprint
from datetime import datetime
from conductor import Conductor
from database import getConfig
import publicclouds


def schedEnable(obj: Conductor):
    print(time.ctime())
    print(obj.getTurnon())
    schedule.every().day.at(obj.getTurnon()).do(obj.enableBroker)


def schedDisable(obj: Conductor):
    print(time.ctime())
    print(obj.getTurnoff())
    schedule.every().day.at(obj.getTurnoff()).do(obj.disableBroker)


def enableNow(obj: Conductor):
    obj.enableBroker()


def disableNow(obj: Conductor):
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


def testCloud(arg:str):
    if arg == 'OCI':
        print(f'Iniciando a verificação de conexão com a {arg}')
        publicclouds.checkOCI()
    else:
        print(f'Sorry, {arg} not yet supported!')


def powerOn(quiet=False):
    clouds = publicclouds.identifyCloud()
    
    for c in clouds:
        if quiet:
            
            print(f'As instancias da {c.upper()} serão iniciada agora!')
            
            if c == 'oci':
                publicclouds.oci('START')
            else:
                print(f'Sorry, {c.upper()} not yet supported!')

        else:
            r = input(f'Deseja ligar as instancias da {c.upper()} agora? [NO/yes]')

            if r.upper() == 'YES' or r.upper() == 'Y':
                if c == 'oci':
                    publicclouds.oci('START')
                else:
                    print(f'Sorry, {c.upper()} not yet supported!')
            else:
                print('Operação cancelada pelo usuário!')


def powerOff(quiet=False):
    clouds = publicclouds.identifyCloud()
    
    for c in clouds:
        if quiet:
            print(f'As instâncias da {c.upper()} serão desligadas agora!')
            
            if c == 'oci':
                publicclouds.oci('STOP')
            else:
                print(f'Sorry, {c.upper()} not yet supported!')

        else:
            r = input(f'Deseja desligar as instâncias da {c.upper()} agora? [NO/yes]')

            if r.upper() == 'YES' or r.upper() == 'Y':
                if c == 'oci':
                    publicclouds.oci('STOP')
                else:
                    print(f'Sorry, {c.upper()} not yet supported!')

            else:
                print('Operação cancelada pelo usuário!')


def main():
    parser = argparse.ArgumentParser(prog='insp-protheus',
                                     usage='%(prog)s [options]',
                                     description='Inspetor Protheus é uma ferramenta para auxiliar na gestão dos serviços',
                                     epilog='%(prog)s está em constante desenvolvimento!')
    
    # group = parser.add_argument_group('Group')
    
    parser.add_argument('-L', '--list',
                        help='Lista as configurações do arquivo settings.json',
                        action='store_true')
    # parser.add_argument('-i','--install',
    #                           help='Instala o inspetor como serviço',
    #                           action='store_false')
    parser.add_argument('-T', '--test-cloud',
                        dest='test_cloud',
                        choices=['TOTVS','AWS', 'AZURE', 'GCP', 'OCI'],
                        help='Valida a conexão com o cloud',
                        action='store')
    parser.add_argument('-off', '--power-off',
                        dest='power_off',
                        help='Desliga as instancias configuradas',
                        action='store_true')
    parser.add_argument('-on', '--power-on',
                        dest='power_on',
                        help='Liga as instancias configuradas',
                        action='store_true')
    parser.add_argument('-r', '--run',
                        help='Executa os agendamentos configurados',
                        action='store_true')
    parser.add_argument('-d', '--disable',
                        help='Desativa todos os serviços configurados agora',
                        action='store_true')
    parser.add_argument('-e', '--enable',
                        help='Ativa todos os serviços configurados agora',
                        action='store_true')
    parser.add_argument('-c','--configure',
                        help='Habilita o mode de configuração',
                        action='store')
    # parser.add_argument('-C','--check-list',
    #                   help='Lista os agendamentos configurados',
    #                   action='store_false')
    # parser.add_argument('-d','--delete',
    #                   help='Deleta todos os agendamentos',
    #                   action='store_false')
    parser.add_argument('-q','--quiet',
                      dest='quiet',
                      help='Executa os processo em modo de sem interação humana',
                      action='store_true')
    parser.add_argument('-v', '--version',
                        action='version',
                        help='Exibe a versão do Inspertor Protheus',
                        version='%(prog)s 0.1')

    args = parser.parse_args()


    if args.list:
        print('O arquivo de configuração...')
        listConfig()
    elif args.test_cloud:
        testCloud(args.test_cloud)
    elif args.power_on:
        powerOn(args.quiet)

    elif args.power_off:
        powerOff(args.quiet)

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
