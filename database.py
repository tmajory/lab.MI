#TODO Cria tabela/classe de depósito com os dados de depósito, endereço e coordenadas
import os
from sqlalchemy import create_engine, ForeignKey, JSON
from sqlalchemy import Column, Integer, Numeric, DateTime, String, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from datetime import datetime

class Base(DeclarativeBase):
    pass


engine = create_engine('sqlite:///database.db',echo=False)

Session = sessionmaker(bind=engine)
session = Session()


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)#Unique e index
    ativo = Column(Boolean, default=True, nullable=False)
    adress = Column(Text, nullable = False)
    longitude = Column(Integer, nullable=False)
    latitude = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    orders = relationship("Orders", back_populates='customers')

    @property
    def __str__(self):
        return f'Cliente: {self.name}, Endereço: {self.adress}, Email: {self.email}, Latitude: {self.latitude}, Longitude: {self.longitude}'

class Veiculos(Base):
    __tablename__ = 'veiculos'

    id = Column(Integer, primary_key = True)
    plate = Column(String(8), nullable=False)
    carga_max = Column(Numeric, nullable=False)
    disponivel = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

class Orders(Base):

    __tablename__ = 'orders'

    id = Column(Integer, nullable=False, primary_key=True)
    peso = Column(Numeric, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.now())
    customer_id = Column(Integer, ForeignKey('customers.id'))
    status = Column(String(20), default='pending')
    customers = relationship("Customers", back_populates="orders")

class Deposito(Base):
    __tablename__ = 'deposito'

    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable=False)
    adress = Column(Text, nullable = False)
    longitude = Column(Integer, nullable=False)
    latitude = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    ativo = Column(Boolean, default=True, nullable=False)

class Planejamento(Base):
    __tablename__ = 'planejamento'

    id = Column(Integer, primary_key = True)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    deposito_id = Column(Integer, ForeignKey('deposito.id'))
    order_id = Column(JSON, ForeignKey('orders.id'), default=list)
    created_at = Column(DateTime, default=datetime.now())
    delivery_date = Column(DateTime, default=None)
    status = Column(String(20), default='pending')



def create_database():

    if not os.path.exists('database.db'):
        Base.metadata.create_all(engine)
        print("Banco de dados criado com sucesso!!")
    else: print("O banco de dados já existe")



if __name__ == '__main__':

    create_database()

    # a = Customers()

    # a.name = 'Joana Darc'
    # a.adress = "Rua dos bobos, 0"
    # a.email = "joanaDarc@yahoo.com"
    # a.latitude = 49000
    # a.longitude = 34562

    # o = Orders()
    # o.customer_id = a
    # o.peso = 50

    # session.add(a)
    # session.commit()
    # session.close()

    # costumers = session.query(Customers).all()
    # orders = session.query(Orders).all()

    # for costumer in costumers:

    #     print(costumer.id, costumer.name, costumer.adress, costumer.latitude, costumer.longitude)
    # session.close()


    # for order in orders:

    #     print(order.id, order.customer_id, order.peso)
    # session.close()

"""
    Implementar um verificador de existência de clientes, de forma, que retorne 
    caso o cliente já exista e caso não o crie.
"""