from util_clientes import cria_cliente
from database import Customers, Orders, session

if __name__ == "__main__":

    c1 = cria_cliente('José Osmar', 'Rua 347, Caucaia, Ceará','zedobrejosantos@gmail.com')

    customers = session.query(Customers).all()
      
    for customer in customers:
        print(customer.id, customer.name, customer.adress, customer.latitude, customer.longitude)
    
    # session.close()
    # print(cliente)