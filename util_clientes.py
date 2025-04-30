#TODO Cadastrar endereço do depósito
#TODO Cadastrar clientes com endereços e busca de coordenadas, exibir clientes no mapa
#TODO Desativar clientes, exibir clientes ativos e inativos  no mapa;
#TODO Cadastrar pedidos, exibir pedidos no mapa;

from geo import retorna_coordenada
from database import Customers, Orders, session


def cria_cliente(nome:str, endereco:str, email:str) -> bool:
    """
    Cria um cliente no banco de dados.
    :param customer: Objeto Customers com os dados do cliente.
    :return: True se o cliente foi criado com sucesso, False caso contrário.
    """
    cliente = Customers()
    cliente.name = nome
    cliente.adress = endereco
    cliente.email = email
    cliente.latitude = retorna_coordenada(endereco)[0]
    cliente.longitude = retorna_coordenada(endereco)[1]

    try:
        session.add(cliente)
        session.commit()
        print(f"Cliente {cliente.name} criado com sucesso!")
        return True
    except Exception as e:
        session.rollback()
        print(f"Erro ao criar cliente: {e}")
        return False
    

def deleta_cliente(email, name):
    session.query(Customers).filter(Customers.email == email, Customers.name == name).update(ativo=False)


def cadastra_pedido(cliente_id:int, peso:float) -> bool:
    """
    Cria um pedido no banco de dados.
    :param cliente_id: ID do cliente que fez o pedido.
    :param peso: Peso do pedido.
    :return: True se o pedido foi criado com sucesso, False caso contrário.
    """
    pedido = Orders()
    pedido.customer_id = cliente_id
    pedido.peso = peso

    try:
        session.add(pedido)
        session.commit()
        print(f"Pedido {pedido.id} criado com sucesso!")
        return True
    except Exception as e:
        session.rollback()
        print(f"Erro ao criar pedido: {e}")
        return False
