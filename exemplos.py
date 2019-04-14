#
from ipv4_network_calculator.ipv4_network_calculator import Ipv4NetworkCalculator

if __name__ == '__main__':
    ### EXEMPLO 1 (Enviando IP com a máscara)
    exemplo1 = Ipv4NetworkCalculator(ip='192.168.60.127', mascara='255.255.255.0')
    exemplo1_tudo: dict = exemplo1.get_all()

    ip: str = exemplo1_tudo['ip']
    prefixo: int = exemplo1_tudo['prefixo']
    mascara: str = exemplo1_tudo['mascara']
    rede: str = exemplo1_tudo['rede']
    broadcast: str = exemplo1_tudo['broadcast']
    numero_ips: int = exemplo1_tudo['numero_ips']

    print("#### EXEMPLO 1 ####")
    print('IP:', ip)
    print('Prefixo:',prefixo)
    print('Máscara:',mascara)
    print('Rede:',rede)
    print('Broadcast:',broadcast)
    print('Número de IPs da rede:',numero_ips)

    ### EXEMPLO 2 (Enviando IP com prefixo)
    exemplo2 = Ipv4NetworkCalculator(ip='10.50.60.224/26')
    exemplo2_tudo: dict = exemplo2.get_all()
    print("\n#### EXEMPLO 2 ####")
    print(exemplo2_tudo)

    ### EXEMPLO 3 (Enviando prefixo separado)
    exemplo3 = Ipv4NetworkCalculator(ip='187.152.12.2', prefixo=30)
    exemplo3_tudo: dict = exemplo3.get_all()
    print("\n#### EXEMPLO 3 ####")
    print(exemplo3_tudo)

    ### EXEMPLO 4 (Usando getters)
    exemplo4 = Ipv4NetworkCalculator('187.152.12.2/30')
    ip: str = exemplo4.ip
    prefixo: int = exemplo4.prefixo
    mascara: str = exemplo4.mascara
    rede: str = exemplo4.rede
    broadcast: str = exemplo4.broadcast
    numero_ips: int = exemplo4.numero_ips

    print("\n#### EXEMPLO 4 ####")
    print(ip, prefixo, mascara, rede, broadcast, numero_ips)

    ### EXEMPLO 5 (Usando setters) e reutilizando a instância
    exemplo5 = Ipv4NetworkCalculator()

    # Set IP/CIDR
    exemplo5.ip = '189.186.25.50/32'
    exemplo5.run() # Precisa executar run
    exemplo5_tudo: dict = exemplo5.get_all()
    print("\n#### EXEMPLO 5.1 ####")
    print(exemplo5_tudo)

    # Set IP e Prefixo separado
    exemplo5.ip = '220.10.20.5'
    exemplo5.prefixo = 24
    exemplo5.run() # Precisa executar run
    exemplo5_tudo: dict = exemplo5.get_all()
    print("\n#### EXEMPLO 5.2 ####")
    print(exemplo5_tudo)

    # Set IP e máscara separados
    exemplo5.ip = '18.1.2.5'
    exemplo5.mascara = '255.255.255.192'
    exemplo5.run() # Precisa executar run
    exemplo5_tudo: dict = exemplo5.get_all()
    print("\n#### EXEMPLO 5.3 ####")
    print(exemplo5_tudo)

    # Set IP sem máscara ou prefixo (vai dar erro)
    exemplo5.ip = '18.118.225.50'
    print("\n#### EXEMPLO 5.4 (Erro) ####")

    try:
        exemplo5.run() # Precisa executar run
        exemplo5: dict = exemplo5.get_all()
        print(exemplo5)
    except ValueError as error:
        print(error)
