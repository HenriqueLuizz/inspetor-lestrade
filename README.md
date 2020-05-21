# inspetor-lestrade

Inspetor Lestrade CLI agendador de tarefas para os serviços do Protheus.

inputs:

- hora de inicio
- recorrencia
- arquivo de configuração

parameters:

- start
- stop
- list
- add
- remove

outputs:

- detail_sched
- status_sched
- next_sched

Realiza a leitura do arquivo .json
Verifica se já tem agendamento no arquivo .json
Se tiver agendamento lista os agendamentos
Se não tiver agendamento pergunta se deseja agendar
