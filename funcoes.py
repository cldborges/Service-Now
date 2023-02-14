import json

def atualizar_credenciais(usuario='', senha=''):
    if usuario =='':
        usuario = input('Qual o usuário?')
    if senha == '':
        senha = input('Qual a senha?')
    with open('conf.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(f'{usuario}\n{senha}')
    print('Usuário e senha atualizados!')


def ler_credenciais():
    with open('conf.txt', 'r', encoding='utf-8') as arquivo:
        usuario, senha = arquivo.readlines()
    return usuario, senha


def relatorio(tipo, nao_remoto):

    # incidentes = 5
    # requests = 10
    # nao_remotos = 1

    # with open('relatorio.txt', 'r', encoding='utf-8') as arquivo:
    #     rel_txt = dict(arquivo.read())
    # print(rel_txt)

    with open('relatorio.json', 'r') as arquivo:
        rel_txt = json.load(arquivo)
    # print(data)
    # print(type(data))

    # my_dict = {'incidentes': 5, 'requests': 10, 'nao_remotos': 1}

    # rel = {'incidentes': 5, 'requests': 10, 'nao_remotos': 1}
    incidentes = rel_txt.get('incidentes')
    requests = rel_txt.get('requests')
    nao_remotos = rel_txt.get('nao_remotos')
    # print(incidentes)

    if tipo == 'incident':
        incidentes += 1
    if tipo == 'request':
        requests += 1
    if nao_remoto == False:
        nao_remotos += 1


    relat = f'Incidentes: {incidentes}\nRequests: {requests}\nPassíveis de remoto: {nao_remotos}'

    rel_atual = {'incidentes': incidentes, 'requests': requests, 'nao_remotos': nao_remotos}

    with open('relatorio.json', 'w') as arquivo:
        json.dump(rel_atual, arquivo)
    # with open('relatorio.txt', 'w', encoding='utf-8') as arquivo:
    #     arquivo.write(relat)
    print(relat)


relatorio('incident', False)