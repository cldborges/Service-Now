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

    incidentes = 5
    requests = 10
    nao_remotos = 1

    relat = f'Incidentes: {incidentes}\nRequests: {requests}\nPassíveis de remoto: {nao_remotos}'
    with open('relatorio.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(relat)
    print(relat)


relatorio('incident', False)