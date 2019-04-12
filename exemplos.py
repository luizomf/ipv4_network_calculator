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

    print('IP:', ip)
    print('Prefixo:',prefixo)
    print('Máscara:',mascara)
    print('Rede:',rede)
    print('Broadcast:',broadcast)
    print('Número de IPs da rede:',numero_ips)

    ### EXEMPLO 2 (Enviando IP com prefixo)
    exemplo2 = Ipv4NetworkCalculator(ip='10.50.60.224/26')
    exemplo2_tudo: dict = exemplo2.get_all()
    print(exemplo2_tudo)

    ### EXEMPLO 3 (Enviando prefixo separado)
    exemplo3 = Ipv4NetworkCalculator(ip='187.152.12.2', prefixo=30)
    exemplo3_tudo: dict = exemplo3.get_all()
    print(exemplo3_tudo)

    ### EXEMPLO 4 (Usando getters)
    exemplo4 = Ipv4NetworkCalculator('187.152.12.2/30')
    ip: str = exemplo4.get_ip()
    prefixo: int = exemplo4.get_prefixo()
    mascara: str = exemplo4.get_mascara()
    rede: str = exemplo4.get_rede()
    broadcast: str = exemplo4.get_broadcast()
    numero_ips: int = exemplo4.get_numero_ips()

    print(ip, prefixo, mascara, rede, broadcast, numero_ips)

    ### EXEMPLO 5 (Usando setters) e reutilizando a instância
    exemplo5 = Ipv4NetworkCalculator()

    # Set IP/CIDR
    exemplo5.set_ip('189.186.25.50/32')
    exemplo5.run() # Precisa executar run
    exemplo5_tudo: dict = exemplo5.get_all()
    print(exemplo5_tudo)

    # Set IP e Prefixo separado
    exemplo5.set_ip('220.10.20.5')
    exemplo5.set_prefixo(24)
    exemplo5.run() # Precisa executar run
    exemplo5_tudo: dict = exemplo5.get_all()
    print(exemplo5_tudo)

    # Set IP e máscara separados
    exemplo5.set_ip('18.1.2.5')
    exemplo5.set_mascara('255.255.255.192')
    exemplo5.run() # Precisa executar run
    exemplo5_tudo: dict = exemplo5.get_all()
    print(exemplo5_tudo)

    # Set IP sem máscara ou prefixo (vai dar erro)
    exemplo5.set_ip('18.118.225.50')
    try:
        exemplo5.run() # Precisa executar run
        exemplo5: dict = exemplo5.get_all()
        print(exemplo5)
    except ValueError as error:
        print(error)

