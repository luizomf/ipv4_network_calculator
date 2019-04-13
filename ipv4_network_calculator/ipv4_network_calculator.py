import re

class Ipv4NetworkCalculator:
    """Obtém todos os dados de uma rede IPv4"""
    def __init__(self, ip: str = '', prefixo: int = 0, mascara: str = ''):
        """Configura os parâmetros (Opcional)"""
        if ip:
            self.__reset()
            self.ip: str = ip
        else:
            self.ip: str = ''

        if prefixo:
            self.prefixo: int = prefixo
        else:
            self.prefixo: int = 0

        if mascara:
            self.mascara: str = mascara
        else:
            self.mascara: str = ''

        self.rede: str = ''
        self.broadcast: str = ''
        self.numero_ips: int = 0

        # Executa tudo caso o IP tenha sido enviado
        if self.ip:
            self.run()

    def __reset(self):
        "Nos casos de reutilização, zera os valores dos atributos e propriedades"
        self.ip: str = ''
        self.mascara: str = ''
        self.prefixo: int = 0
        self.broadcast: str = ''
        self.rede: str = ''
        self.numero_ips: int = 0

    def run(self):
        """Executa tudo"""

        # Sem IP, sem cálculo
        if self.ip == '' or not self.ip:
            raise ValueError("IP não enviado.")

        # Extrai o prefixo do IP caso IP tenha o formato IP/CIDR
        self.__set_prefixo_do_ip()

        if not self.prefixo and not self.mascara:
            raise ValueError("Ou o prefixo ou a máscara devem ser enviados.")

        # Caso a máscara tenha sido enviada, extrai o prefixo da máscara
        if self.mascara:
            self.__mascara_bin = self.__ip_decimal_para_binario(ip=self.mascara)
            self.__set_prefixo_da_mascara()

        self.__set_numero_ips()
        self.__set_rede_broadcast()
        self.__set_mascara_do_prefixo()

    def __set_mascara_do_prefixo(self):
        """Configura O IP da máscara usando o prefixo."""
        mascara_bin: str = ''

        # Liga os bits da máscara até o tamanho do prefixo
        # Desliga os restantes
        for i in range(32):
            if i < int(self.prefixo):
                mascara_bin += '1'
            else:
                mascara_bin += '0'

        # Converte a máscara para decimal
        mascara_dec: str = self.__ip_binario_para_decimal(mascara_bin)
        self.mascara: str = mascara_dec

    def __set_rede_broadcast(self):
        """Configura rede e broadcast"""
        ip_bin: str = self.__ip_decimal_para_binario(self.ip)
        ip_bin: str = ip_bin.replace('.', '')

        # Seta as variáveis para receber os bits
        rede: str = ''
        broadcast: str = ''

        # Passa por cada bit do IP
        # Até o tamanho do prefixo,
        # Rede e broadcast tem os mesmos
        # bits do IP.
        # Os bits finais são desligados para rede e ligados para broadcast
        for conta, bit in enumerate(ip_bin):
            if conta < int(self.prefixo):
                rede += str(bit)
                broadcast += str(bit)
            else:
                rede += '0'
                broadcast += '1'

        self.rede: str = self.__ip_binario_para_decimal(rede)
        self.broadcast: str = self.__ip_binario_para_decimal(broadcast)

    def __set_numero_ips(self):
        """Configura o número de hosts para a rede"""
        host_bits: int = 32-int(self.prefixo)
        self.numero_ips: int = pow(2, host_bits)

    def __set_prefixo_da_mascara(self):
        """Configura o prefixo baseado nos bits ligados do
        IP da máscara"""
        mascara_bin: str = self.__mascara_bin.replace('.', '')
        conta: int = 0

        for bit in mascara_bin:
            if bit == '1':
                conta += 1

        self.prefixo: int = conta

    def __ip_binario_para_decimal(self, ip: str = '') -> str:
        """Converte um IP binário para decimal"""
        novo_ip: str = str(int(ip[0:8], 2)) + '.'
        novo_ip += str(int(ip[8:16], 2)) + '.'
        novo_ip += str(int(ip[16:24], 2)) + '.'
        novo_ip += str(int(ip[24:32], 2))

        return novo_ip

    def __ip_decimal_para_binario(self, ip: str = '') -> str:
        """Converte um IP decimal para binário"""
        if not ip:
            ip: str = self.ip

        # Divide o IP em 4 blocos
        bloco_ip: list = ip.split('.')
        ip_bin: list = []

        for bloco in bloco_ip:
            # Converte o bloco para binário
            binario: bin = bin(int(bloco))
            # Forma o octeto
            binario: bin = binario[2:].zfill(8)
            ip_bin.append(binario)

        # TODO: retornar sem o ponto
        ip_com_pontos: str = '.'.join(ip_bin)
        return ip_com_pontos

    def __set_prefixo_do_ip(self) -> bool:
        """Verifica se o IP tem prefixo."""
        ip_prefixo_regexp = re.compile('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,2}$')

        if not ip_prefixo_regexp.search(self.ip):
            return False

        divide_ip = self.ip.split('/')
        self.ip = divide_ip[0]
        self.prefixo = divide_ip[1]

        return True

    def __is_ip(self, ip) -> bool:
        """Verifica se o IP é válido."""
        if not ip:
            return False

        # Aceita IP ou IP/CIDR (Ex.: 192.168.0.1 ou 192.168.0.1/24)
        ip_regexp = re.compile('^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})(/[0-9]{1,2})?$')

        if ip_regexp.search(ip):
            return True
        return False

    ## GETTERS
    @property
    def ip(self) -> str:
        return str(self.__ip)

    @property
    def prefixo(self) -> int:
        return int(self.__prefixo)

    @property
    def mascara(self) -> str:
        return str(self.__mascara)

    def get_all(self):
        """Retorna tudo que foi configurado, caso necessário."""
        all: dict = {
            'ip': self.ip,
            'prefixo': self.prefixo,
            'mascara': self.mascara,
            'rede': self.rede,
            'broadcast': self.broadcast,
            'numero_ips': self.numero_ips,
        }

        return all

    # SETTERS
    @ip.setter
    def ip(self, ip: str = ''):
        if ip:
            if not self.__is_ip(ip):
                raise ValueError("IP inválido")

            self.__reset()
            self.__ip: str = str(ip)
        else:
            self.__ip = ''

    @prefixo.setter
    def prefixo(self, prefixo: int = 0):
        if prefixo:
            self.__prefixo: int = int(prefixo)

            if not self.ip:
                raise ValueError("Setar IP primeiro.")
        else:
            self.__prefixo = 0

    @mascara.setter
    def mascara(self, mascara: str = ''):
        if mascara:
            if not self.__is_ip(mascara):
                raise ValueError("Máscara inválida")

            self.__mascara: str = str(mascara)

            if not self.ip:
                raise ValueError("Setar IP primeiro.")
        else:
            self.__mascara = ''
