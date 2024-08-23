from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated=['auto'])

def verificar_senha(senha: str, hash_senha: str):
    '''
    Função para verficar se a senha esta correta, comparando a senha em texto puro,
    informado pelo usuario e o hash da senha que estara salvo no banco de dados durante
    a criação da conta
    '''
    return CRIPTO.verify(senha, hash_senha)

def gerar_hash(senha: str):
    '''
    funcão que gera e retorna o hash da senha
    '''

    return CRIPTO.hash(senha)