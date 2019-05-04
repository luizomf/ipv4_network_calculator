import re
from typing import Union


class Ipv4NetworkCalculator:
    """Obtém todos os dados de uma rede IPv4"""

    __slots__ = ('_ip', '_mascara', '_prefixo', '_broadcast',
                 '_numero_ips', '_rede', '_ip_bin', '_mascara_bin',
                 '_rede_bin', '_broadcast_bin')

    def __init__(self, ip: str = '', prefixo: int = 0, mascara: str = ''):
        """Configura os parâmetros e executa caso IP tenha sido enviado

        :param ip: o ip (pode conter barra e prefixo, como /24)
        :type ip: str
        :param prefixo: o prefixo pode ser enviado separadamente (opcional)
        :type prefixo: int
        :param mascara: o ip da máscara de sub-rede (opcional)
        :type mascara: str
        """
        if ip:
            self._reset()
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

        self._rede: str = ''
        self._broadcast: str = ''
        self._numero_ips: int = 0

        # Executa tudo caso o IP tenha sido enviado
        if self.ip:
            self.run()

    def _reset(self):
        """Nos casos de reutilização, zera os valores dos
        atributos e propriedades"""
        self._ip: str = ''
        self._mascara: str = ''
        self._prefixo: int = 0
        self._broadcast: str = ''
        self._rede: str = ''
        self._numero_ips: int = 0

    def run(self):
        """Realiza os cálculos

        Se o atributo ip e/ou (máscara ou prefixo) não forem enviados
        ao instanciar a classe para reutilização da instancia, será
        necessário atribuir os valores de ip, prefixo ou máscara
        posteriormente. Nesses casos é necessário executar este
        método para realização do cálculo."""

        # Sem IP, sem cálculo
        if self.ip == '' or not self.ip:
            raise ValueError("IP não enviado.")

        # Extrai o prefixo do IP caso IP tenha o formato IP/CIDR
        self._set_prefixo_do_ip()

        if not self._prefixo and not self._mascara:
            raise ValueError("Ou o prefixo ou a máscara devem ser enviados.")

        # Caso a máscara tenha sido enviada, extrai o prefixo da máscara
        if self._mascara:
            self._mascara_bin = self._ip_decimal_para_binario(ip=self._mascara)
            self._set_prefixo_da_mascara()

        self._set_numero_ips()
        self._set_rede_broadcast()
        self._set_mascara_do_prefixo()

    def _set_mascara_do_prefixo(self):
        """Configura O IP da máscara usando o prefixo."""
        mascara_bits = self.prefixo * str('1')
        host_bits = (32 - self.prefixo) * str('0')

        self._mascara_bin = self._binario_adiciona_pontos(
            mascara_bits + host_bits)

        # Converte a máscara para decimal
        mascara_dec: str = self._ip_binario_para_decimal(self._mascara_bin)
        self._mascara: str = mascara_dec

    def _set_rede_broadcast(self):
        """Configura rede e broadcast"""
        ip_bin: str = self._ip_decimal_para_binario(self.ip)
        ip_bin: str = ip_bin.replace('.', '')

        ip_bits = ip_bin[:self._prefixo]
        host_bits = 32 - self.prefixo
        rede = ip_bits + (str('0') * host_bits)
        broadcast = ip_bits + (str('1') * host_bits)

        self._ip_bin = self._binario_adiciona_pontos(ip_bin)
        self._rede_bin = self._binario_adiciona_pontos(rede)
        self._broadcast_bin = self._binario_adiciona_pontos(broadcast)

        self._rede: str = self._ip_binario_para_decimal(rede)
        self._broadcast: str = self._ip_binario_para_decimal(broadcast)

    def _binario_adiciona_pontos(self, b: str) -> str:
        """Adiciona pontos aos octetos

        :param b: IP em binário sem pontos
        :type b: str
        :return: IP em binário com pontos
        :rtype: str
        """
        b: str = re.sub('[^0-1]', '', b)
        return f'{b[0:8]}.{b[8:16]}.{b[16:24]}.{b[24:32]}'

    def _set_numero_ips(self):
        """Configura o número de hosts para a rede"""
        host_bits: int = 32 - int(self._prefixo)
        self._numero_ips: int = pow(2, host_bits)

    def _set_prefixo_da_mascara(self):
        """Configura o prefixo baseado nos bits ligados do
        IP da máscara"""
        mascara_bin: str = self._mascara_bin.replace('.', '')
        conta: int = int(mascara_bin.count('1'))

        self._prefixo: int = conta

    def _ip_binario_para_decimal(self, ip: str = '') -> str:
        """Converte um IP binário para decimal

        :param ip: o número do IP em binário
        :type ip: str
        :return: O IP em decimal.
        :rtype: str
        """
        ip: str = re.sub('[^0-9]', '', ip)

        novo_ip: str = str(int(ip[0:8], 2)) + '.'
        novo_ip += str(int(ip[8:16], 2)) + '.'
        novo_ip += str(int(ip[16:24], 2)) + '.'
        novo_ip += str(int(ip[24:32], 2))

        return novo_ip

    def _ip_decimal_para_binario(self, ip: str = '') -> str:
        """Converte um IP decimal para binário

        :param ip: O IP em decimal
        :type ip: str
        :return: O IP em binário
        :rtype: str
        """
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

        ip_bin: str = '.'.join(ip_bin)
        return ip_bin

    def _set_prefixo_do_ip(self) -> bool:
        """Verifica se o IP tem prefixo.

        :return: True se o IP tiver prefixo, False caso contrário.
        :rtype: bool
        """
        ip_prefixo_regexp = re.compile(
            '^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,2}$'
        )

        if not ip_prefixo_regexp.search(self.ip):
            return False

        divide_ip = self.ip.split('/')
        self.ip = divide_ip[0]
        self.prefixo = int(divide_ip[1])

        return True

    def _is_ip(self, ip) -> bool:
        """Verifica se o IP é válido.

        :param ip: O IP em decimal
        :type ip: str
        :return: True se o IP estiver correto, False caso contrário.
        :rtype: bool
        """
        if not ip:
            return False

        clean_ip = re.sub('/[0-9]+', '', ip)
        blocos = clean_ip.split('.')

        for bloco in blocos:
            bloco = int(bloco)

            if bloco < 0 or bloco > 255:
                return False

        return True

    def _check_property(self, property: Union[str, int]):
        """Verifica se existe o valor de uma propriedade

        :param property: qualquer propriedade da classe
        :type property: Union[str, int]
        """
        if not property:
            raise ValueError("Valor usado incorretamente. "
                             "Envie IP, máscara ou prefixo e "
                             "execute run().")

    # GETTERS
    @property
    def ip(self) -> str:
        return str(self._ip)

    @property
    def prefixo(self) -> int:
        return int(self._prefixo)

    @property
    def mascara(self) -> str:
        return str(self._mascara)

    # Read only
    @property
    def rede(self) -> str:
        self._check_property(self._rede)
        return str(self._rede)

    @property
    def broadcast(self) -> str:
        self._check_property(self._broadcast)
        return str(self._broadcast)

    @property
    def numero_ips(self) -> str:
        self._check_property(self._numero_ips)
        return str(self._numero_ips)

    @property
    def ip_bin(self) -> str:
        self._check_property(self._ip_bin)
        return str(self._ip_bin)

    @property
    def mascara_bin(self) -> str:
        self._check_property(self._mascara_bin)
        return str(self._mascara_bin)

    @property
    def rede_bin(self) -> str:
        self._check_property(self._rede_bin)
        return str(self._rede_bin)

    @property
    def broadcast_bin(self) -> str:
        self._check_property(self._broadcast_bin)
        return str(self._broadcast)

    def get_all(self):
        """ Retorna tudo que foi configurado, caso necessário.

        :return: um dicionário com os dados calculados.
        :rtype: dict
        """
        all: dict = {
            'ip': self.ip,
            'prefixo': self._prefixo,
            'mascara': self._mascara,
            'rede': self._rede,
            'broadcast': self._broadcast,
            'numero_ips': self._numero_ips,
        }

        return all

    def get_all_bin(self):
        """ Retorna tudo que foi configurado em binário.

        :return: um dicionário com os dados calculados.
        :rtype: dict
        """
        all: dict = {
            'ip': self._ip_bin,
            'mascara': self._mascara_bin,
            'rede': self._rede_bin,
            'broadcast': self._broadcast_bin,
        }

        return all

    # SETTERS
    @ip.setter
    def ip(self, ip: str = ''):
        if ip:
            if not self._is_ip(ip):
                raise ValueError("IP inválido")

            self._reset()
            self._ip: str = str(ip)
        else:
            self._ip = ''

    @prefixo.setter
    def prefixo(self, prefixo: int = 0):
        if prefixo:
            if not self.ip:
                raise ValueError("Setar IP primeiro.")

            if prefixo > 32:
                raise ValueError("Prefixo inválido")

            self._prefixo: int = int(prefixo)
        else:
            self._prefixo = 0

    @mascara.setter
    def mascara(self, mascara: str = ''):
        if mascara:
            if not self._is_ip(mascara):
                raise ValueError("Máscara inválida")

            if not self.ip:
                raise ValueError("Setar IP primeiro.")

            self._mascara: str = str(mascara)
        else:
            self._mascara = ''
