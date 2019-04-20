# ipv4_network_calculator
Realiza cálculo de máscara de sub-rede IPv4 em Python baseando-se no IP/CIDR ou IP/Máscara.

Retorna vários valores úteis: IP, Prefixo, Máscara, IP da rede e de broadcast, número máximo
de IPs da rede, e os binários do IP, Máscara, Rede e Broadcast.

Criado como parte de um vídeo tutorial disponível em https://youtu.be/wI-tdeDPGlU

Exemplos de uso no arquivo exemplos.py

# Exemplos de uso
A classe está separada na subpasta `ipv4_network_calculator`.
## Import
Antes de qualquer coisa:
```
from SUAPASTA.ipv4_network_calculator import Ipv4NetworkCalculator
```
Você também pode renomear o arquivo principal e a classe caso sinta necessidade.

Existem vários modos de uso para essa mesma classe, vou listar vários deles a seguir.
## Exemplo 1: enviando IP e máscara - get_all()
```
exemplo1 = Ipv4NetworkCalculator(
    ip='192.168.60.127',
    mascara='255.255.255.0')
exemplo1_tudo: dict = exemplo1.get_all()

ip: str = exemplo1_tudo['ip']
prefixo: int = exemplo1_tudo['prefixo']
mascara: str = exemplo1_tudo['mascara']
rede: str = exemplo1_tudo['rede']
broadcast: str = exemplo1_tudo['broadcast']
numero_ips: int = exemplo1_tudo['numero_ips']

print("#### EXEMPLO 1 ####")
print('IP:', ip)
print('Prefixo:', prefixo)
print('Máscara:', mascara)
print('Rede:', rede)
print('Broadcast:', broadcast)
print('Número de IPs da rede:', numero_ips)
```
## Exemplo 2: enviando IP/Prefixo
```
exemplo2 = Ipv4NetworkCalculator(ip='10.50.60.224/26')
exemplo2_tudo: dict = exemplo2.get_all()
print(exemplo2_tudo)
```
## Exemplo 3: enviando IP e prefixo separados
```
exemplo3 = Ipv4NetworkCalculator(ip='187.152.12.2', prefixo=30)
exemplo3_tudo: dict = exemplo3.get_all()
print(exemplo3_tudo)
```
## Exemplo 4: usando getters
```
exemplo4 = Ipv4NetworkCalculator('187.152.12.2/30')
ip: str = exemplo4.ip
prefixo: int = exemplo4.prefixo
mascara: str = exemplo4.mascara
rede: str = exemplo4.rede
broadcast: str = exemplo4.broadcast
numero_ips: int = exemplo4.numero_ips

print(ip, prefixo, mascara, rede, broadcast, numero_ips)
 ```
## Exemplo 5: vários outros exemplos
```
# EXEMPLO 5 (Usando setters) e reutilizando a instância
exemplo5 = Ipv4NetworkCalculator()

# Set IP/CIDR
exemplo5.ip = '189.186.25.50/32'
exemplo5.run()  # Precisa executar run
exemplo5_tudo: dict = exemplo5.get_all()
print("\n#### EXEMPLO 5.1 ####")
print(exemplo5_tudo)

# Set IP e Prefixo separado
exemplo5.ip = '220.10.20.5'
exemplo5.prefixo = 24
exemplo5.run()  # Precisa executar run
exemplo5_tudo: dict = exemplo5.get_all()
print("\n#### EXEMPLO 5.2 ####")
print(exemplo5_tudo)

# Set IP e máscara separados
exemplo5.ip = '18.1.2.5'
exemplo5.mascara = '255.255.255.192'
exemplo5.run()  # Precisa executar run
exemplo5_tudo: dict = exemplo5.get_all()
print("\n#### EXEMPLO 5.3 ####")
print(exemplo5_tudo)

# Set IP sem máscara ou prefixo (vai dar erro)
exemplo5.ip = '18.118.225.50'
print("\n#### EXEMPLO 5.4 (Erro) ####")

try:
    exemplo5.run()  # Precisa executar run
    exemplo5: dict = exemplo5.get_all()
    print(exemplo5)
except ValueError as error:
    print(error)
```
## Exemplo 6: retornando binários
```
exemplo6 = Ipv4NetworkCalculator(ip='192.168.25.127', prefixo=24)
exemplo6_tudo_bin: dict = exemplo6.get_all_bin()
exemplo6_tudo_dec: dict = exemplo6.get_all()
print(exemplo6_tudo_bin)
print(exemplo6_tudo_dec)
```
