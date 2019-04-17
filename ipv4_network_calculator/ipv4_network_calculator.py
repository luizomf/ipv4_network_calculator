import re


class Ipv4NetworkCalculator:
    """Obtém todos os dados de uma rede IPv4"""

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

        self.rede: str = ''
        self.broadcast: str = ''
        self.numero_ips: int = 0

        # Executa tudo caso o IP tenha sido enviado
        if self.ip:
            self.run()

    def _reset(self):
        """Nos casos de reutilização, zera os valores dos
        atributos e propriedades"""
        self._ip: str = ''
        self._mascara: str = ''
        self._prefixo: int = 0
        self.ip: str = ''
        self.mascara: str = ''
        self.prefixo: int = 0
        self.broadcast: str = ''
        self.rede: str = ''
        self.numero_ips: int = 0

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

        if not self.prefixo and not self.mascara:
            raise ValueError("Ou o prefixo ou a máscara devem ser enviados.")

        # Caso a máscara tenha sido enviada, extrai o prefixo da máscara
        if self.mascara:
            self._mascara_bin = self._ip_decimal_para_binario(ip=self.mascara)
            self._set_prefixo_da_mascara()

        self._set_numero_ips()
        self._set_rede_broadcast()
        self._set_mascara_do_prefixo()

    def _set_mascara_do_prefixo(self):
        """Configura O IP da máscara usando o prefixo."""
        mascara_bin: str = ''

        # Liga os bits da máscara até o tamanho do prefixo
        # Desliga os restantes
        for i in range(32):
            if i < int(self.prefixo):
                mascara_bin += '1'
            else:
                mascara_bin += '0'

        self.mascara_bin = self._binario_adiciona_pontos(mascara_bin)

        # Converte a máscara para decimal
        mascara_dec: str = self._ip_binario_para_decimal(mascara_bin)
        self.mascara: str = mascara_dec

    def _set_rede_broadcast(self):
        """Configura rede e broadcast"""
        ip_bin: str = self._ip_decimal_para_binario(self.ip)
        ip_bin: str = ip_bin.replace('.', '')

        # Seta as variáveis para receber os bits
        ip: str = ''
        rede: str = ''
        broadcast: str = ''

        # Passa por cada bit do IP
        # Até o tamanho do prefixo,
        # Rede e broadcast tem os mesmos
        # bits do IP.
        # Os bits finais são desligados para rede e ligados para broadcast
        for conta, bit in enumerate(ip_bin):
            ip += str(bit)
            if conta < int(self.prefixo):
                rede += str(bit)
                broadcast += str(bit)
            else:
                rede += '0'
                broadcast += '1'

        self.ip_bin = self._binario_adiciona_pontos(ip)
        self.rede_bin = self._binario_adiciona_pontos(rede)
        self.broadcast_bin = self._binario_adiciona_pontos(broadcast)

        self.rede: str = self._ip_binario_para_decimal(rede)
        self.broadcast: str = self._ip_binario_para_decimal(broadcast)

    def _binario_adiciona_pontos(self, b: str) -> str:
        """Adiciona pontos aos octetos

        :param b: IP em binário sem pontos
        :type b: str
        :return: IP em binário com pontos
        :rtype: str
        """
        return '{}.{}.{}.{}'.format(b[0:8], b[8:16], b[16:24], b[24:32])

    def _set_numero_ips(self):
        """Configura o número de hosts para a rede"""
        host_bits: int = 32 - int(self.prefixo)
        self.numero_ips: int = pow(2, host_bits)

    def _set_prefixo_da_mascara(self):
        """Configura o prefixo baseado nos bits ligados do
        IP da máscara"""
        mascara_bin: str = self._mascara_bin.replace('.', '')
        conta: int = 0

        for bit in mascara_bin:
            if bit == '1':
                conta += 1

        self.prefixo: int = conta

    def _ip_binario_para_decimal(self, ip: str = '') -> str:
        """Converte um IP binário para decimal

        :param ip: o número do IP em binário
        :type ip: str
        :return: O IP em decimal.
        :rtype: str
        """
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
        self.prefixo = divide_ip[1]

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

        # Aceita IP ou IP/CIDR (Ex.: 192.168.0.1 ou 192.168.0.1/24)
        ip_regexp = re.compile(
            '^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})(/[0-9]{1,2})?$'
        )

        if ip_regexp.search(ip):
            return True
        return False

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

    def get_all(self):
        """ Retorna tudo que foi configurado, caso necessário.

        :return: um dicionário com os dados calculados.
        :rtype: dict
        """
        all: dict = {
            'ip': self.ip,
            'prefixo': self.prefixo,
            'mascara': self.mascara,
            'rede': self.rede,
            'broadcast': self.broadcast,
            'numero_ips': self.numero_ips,
        }

        return all

    def get_all_bin(self):
        """ Retorna tudo que foi configurado em binário.

        :return: um dicionário com os dados calculados.
        :rtype: dict
        """
        all: dict = {
            'ip': self.ip_bin,
            'mascara': self.mascara_bin,
            'rede': self.rede_bin,
            'broadcast': self.broadcast_bin,
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
            self._prefixo: int = int(prefixo)

            if not self.ip:
                raise ValueError("Setar IP primeiro.")
        else:
            self._prefixo = 0

    @mascara.setter
    def mascara(self, mascara: str = ''):
        if mascara:
            if not self._is_ip(mascara):
                raise ValueError("Máscara inválida")

            self._mascara: str = str(mascara)

            if not self.ip:
                raise ValueError("Setar IP primeiro.")
        else:
            self._mascara = ''
