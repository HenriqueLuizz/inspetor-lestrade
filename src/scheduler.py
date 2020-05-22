    # """Zere os segundos de now e some mais 1 minuto."""
    # new_target = datetime.now().replace(second=0, microsecond=0)
    # new_target += timedelta(minutes=1)
    # print(new_target)

    # scheduler.enterabs(new_target.timestamp(),
    #                    priority=100,
    #                    action=google_request)


"""Agendador de Tarefas Protheus

Definir a data e hora de iniciar ou parar serviço

- Informar a data e hora
- Informar o evento (Para ou Iniciar)


"""

"""Marcar um evento em um tempo específico."""
import sched
import time
from datetime import datetime, timedelta

scheduler = sched.scheduler(timefunc=time.time)

def reschedule(moment, task):
    
    scheduler.enterabs(moment,
                       priority=100,
                       action=task)

def runschedule():
    try:
        scheduler.run(blocking=True) #blocking=False
    except KeyboardInterrupt:
        print('Parei com sched')
