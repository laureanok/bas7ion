import unittest

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver
from bastion.networking.base import Networking
from bastion.test.utils import VAULT_TOKEN_TEST


class VpnTest(unittest.TestCase):

    def test_vpn(self):
        # Se obtienen las credenciales
        auth_driver = VaultAuthDriver(VAULT_TOKEN_TEST)
        providers_cred = auth_driver.get_providers_info('secret/projectVPN/')
        # Se obtiene driver
        driver1 = Driver.create(providers_cred[0])
        driver2 = Driver.create(providers_cred[1])
        # Se crea la red 1
        network1 = driver1.networking.create_network(name="Bas7ionVPC-VPN-1",
                                                     cidr="10.0.0.0/16")
        # Se crea las subred de la red 1
        subnet1 = network1.create_subnet(name="Bas7ionSubnet-VPN-1",
                                         cidr="10.0.1.0/24")
        # Se crea la maquina virtual
        driver1.baseCompute.create_vm(name="Bas7ionVM-VPN-1",
                                      subnet=subnet1)
        # Se crea la red 2
        network2 = driver2.networking.create_network(name="Bas7ionVPC-VPN-2",
                                                     cidr="20.0.0.0/16")
        # Se crea las subred de la red 2
        subnet2 = network2.create_subnet(name="Bas7ionSubnet-VPN-2",
                                         cidr="20.0.1.0/24")
        # Se crea la maquina virtual
        driver2.baseCompute.create_vm(name="Bas7ionVM-VPN-2",
                                      subnet=subnet2)
        Networking.connect_networks(network1, network2)
