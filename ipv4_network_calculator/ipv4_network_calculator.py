import re

class Ipv4NetworkCalculator():
    """Obtém todos os dados de uma rede IPv4"""
    def __init__(self, ip: str = '', prefixo: int = 0, mascara: str = ''):
        """
        Parameters
        ----------
        ip : str
            um IP na versão 4. Ex.: 192.168.0.1.
            O IP também pode vir com prefixo (192.168.0.1/24), nesse caso
            não é necessário enviar o parâmetro do prefixo.
        prefixo : int
            o prefixo da rede. Ex.: 24, 8, 30 (não necessário se enviar a máscara
            ou o prefixo via IP)
        mascara : str
            a mascara de sub-rede. Ex.: 255.255.255.0 (não necessário se enviar o prefixo
            via IP ou parâmetro)
        """
        self.__ip: str = ip
        self.__prefixo: int = prefixo
        self.__mascara: str = mascara

        self.__rede: str = ''
        self.__broadcast: str = ''
        self.__numero_ips: int = 0

        # Executa tudo
        if self.__ip:
            self.run()

    def __reset(self):
        self.__mascara: str = ''
        self.__prefixo: int = 0
        self.__broadcast: str = ''
        self.__rede: str = ''
        self.__numero_ips: int = 0

    def run(self):
        if self.__ip == '' or not self.__ip:
            raise ValueError("IP não enviado.")

        self.__ip_tem_prefixo()

        if not self.__is_ip():
            raise ValueError("IP inválido.")

        if not self.__prefixo and not self.__mascara:
            raise ValueError("Ou o prefixo ou a máscara devem ser enviados.")

        if self.__mascara:
            self.__mascara_bin = self.__ip_decimal_para_binario(ip=self.__mascara)
            self.__set_prefixo_da_mascara()

        self.__set_numero_ips()
        self.__set_rede_broadcast()
        self.__set_mascara_do_prefixo()

    def __set_mascara_do_prefixo(self):
        """Configura O IP da máscara de sub-rede"""
        mascara_bin: str = ''

        # Liga os bits da máscara até o tamanho do prefixo
        # Desliga os restantes
        for i in range(32):
            if i < int(self.__prefixo):
                mascara_bin += '1'
            else:
                mascara_bin += '0'

        mascara_dec: str = self.__ip_binario_para_decimal(mascara_bin)

        self.__mascara: str = mascara_dec

    def __set_rede_broadcast(self):
        """Configura rede e broadcast"""
        ip_bin: str = self.__ip_decimal_para_binario(self.__ip)
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
            if conta < int(self.__prefixo):
                rede += str(bit)
                broadcast += str(bit)
            else:
                rede += '0'
                broadcast += '1'

        self.__rede: str = self.__ip_binario_para_decimal(rede)
        self.__broadcast: str = self.__ip_binario_para_decimal(broadcast)

    def __set_numero_ips(self):
        """Configura o número de hosts para a rede"""
        host_bits: int = 32-int(self.__prefixo)
        self.__numero_ips: int = pow(2, host_bits)

    def __set_prefixo_da_mascara(self):
        """Configura o prefixo baseado nos bits ligados do
        IP da máscara"""
        mascara_bin: str = self.__mascara_bin.replace('.', '')
        conta: int = 0

        for bit in mascara_bin:
            if bit == '1':
                conta += 1

        self.__prefixo: int = conta

    def __ip_binario_para_decimal(self, ip: str = '') -> str:
        """Converte um IP binário para decimal

        Parameters
        ----------
        ip : str
            O IP em números binários

        Returns
        -------
        str
            o IP em decimal
        """
        novo_ip: str = str(int(ip[0:8], 2)) + '.'
        novo_ip += str(int(ip[8:16], 2)) + '.'
        novo_ip += str(int(ip[16:24], 2)) + '.'
        novo_ip += str(int(ip[24:32], 2))

        return novo_ip

    def __ip_decimal_para_binario(self, ip: str = '') -> str:
        """Converte um IP decimal para binário

        Parameters
        ----------
        ip : str
            O IP em decimal

        Returns
        -------
        str
            o IP em binário
        """
        if not ip:
            ip: str = self.__ip

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

    def __ip_tem_prefixo(self) -> bool:
        """Verifica se o IP tem prefixo.
        Se tiver, configura o ip e prefixo.

        Returns
        -------
        Bool
            Se o IP tiver prefixo, True. False caso não tenha.
        """
        ip_prefixo_regexp = re.compile('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,2}$')

        if not ip_prefixo_regexp.search(self.__ip):
            return False

        divide_ip = self.__ip.split('/')
        self.__ip = divide_ip[0]
        self.__prefixo = divide_ip[1]

        return True

    def __is_ip(self) -> bool:
        """Verifica se o IP tem prefixo.
        Se tiver, configura o ip e prefixo.

        Returns
        -------
        bool
            True se o IP estiver correto, False caso contrário.
        """
        ip_regexp = re.compile('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$')

        if ip_regexp.search(self.__ip):
            return True
        return False

    ## GETTERS
    def get_ip(self) -> str:
        return str(self.__ip)

    def get_prefixo(self) -> int:
        return int(self.__prefixo)

    def get_mascara(self) -> str:
        return str(self.__mascara)

    def get_rede(self) -> str:
        return str(self.__rede)

    def get_broadcast(self) -> str:
        return str(self.__broadcast)

    def get_numero_ips(self) -> int:
        return int(self.__numero_ips)

    def get_all(self):
        """Retorna tudo que foi configurado."""
        return {
            'ip': self.get_ip(),
            'prefixo': self.get_prefixo(),
            'mascara': self.get_mascara(),
            'rede': self.get_rede(),
            'broadcast': self.get_broadcast(),
            'numero_ips': self.get_numero_ips(),
        }

    # SETTERS
    def set_ip(self, ip: str = ''):
        self.__ip: str = str(ip)
        self.__reset()

    def set_prefixo(self, prefixo: int = 0):
        if not self.__ip:
            raise ("Setar IP primeiro.")

        self.__reset()
        self.__prefixo: int = int(prefixo)

    def set_mascara(self, mascara: str = ''):
        if not self.__ip:
            raise ("Setar IP primeiro.")

        self.__reset()
        self.__mascara: str = str(mascara)

