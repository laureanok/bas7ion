# Test AWS DNS

import unittest

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver
from bastion.test.utils import VAULT_TOKEN_TEST


class TestDNS(unittest.TestCase):

    def test_dns(self):

        auth_driver = VaultAuthDriver(VAULT_TOKEN_TEST)
        cred = auth_driver.get_provider_info('secret/projectDNS/cred1')

        # Se obtiene driver
        driver = Driver.create(cred)

        # Se crea la red
        network = driver.networking.create_network(name="Bas7ionNetwork-DNS",
                                                   cidr="30.0.0.0/16")

        # Se crean las subredes
        subnet1 = network.create_subnet(name="Bas7ionSubnet1-DNS",
                                        cidr="30.0.1.0/24")
        subnet2 = network.create_subnet(name="Bas7ionSubnet2-DNS",
                                        cidr="30.0.2.0/24")

        # Se crean las maquinas virtuales
        vm1 = driver.baseCompute.create_vm(name="Bas7ionVM1-DNS",
                                           subnet=subnet1)
        vm2 = driver.baseCompute.create_vm(name="Bas7ionVM2-DNS",
                                           subnet=subnet2)
        # Se agregan los mombres de las VM
        vm1.add_hostname("Bas7ionVM1-DNS-hostname", "bas7ion.com")
        vm2.add_hostname("Bas7ionVM2-DNS-hostname", "bas7ion.com")
