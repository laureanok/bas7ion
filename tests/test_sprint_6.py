# Test Sprint 5

import unittest

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver


class TestSprint6(unittest.TestCase):

    def test_sprint_6(self):
        auth_driver = VaultAuthDriver('token', 'bas7ion')
        provider_creds = auth_driver.get_providers_info()

        # Se obtiene driver de Amazon
        aws_driver = Driver.create(provider_creds[0])

        # Se crea la red en Amazon
        aws_bastion_vpc = aws_driver.networking.create_network(name="vpn_bastion_vpc",
                                                               cidr="16.16.0.0/16")

        # Se crea la subred privada en Amazon
        aws_bastion_priv_subnet = aws_bastion_vpc.create_subnet(name="vpn_bastion_priv_subnet",
                                                                cidr="16.16.2.0/24")

        # Se crea la maquina virtual en la subred privada en amazon
        aws_driver.baseCompute.create_vm(name="vpn_bastion_vm_priv",
                                         subnet=aws_bastion_priv_subnet,
                                         public_key_file_path='/Volumes/Datos/Users/diegomendez29/.ssh/id_rsa.pub')

        # Se obtiene driver de Azure
        azure_driver = Driver.create(provider_creds[1])

        # Se crea la red en Azure
        azure_bastion_vpc = azure_driver.networking.create_network(name="bastion_vpc",
                                                                   cidr="10.1.0.0/16")

        # Se crea la subred rn Azure
        azure_bastion_priv_subnet = azure_bastion_vpc.create_subnet(name="bastion_priv_subnet",
                                                                    cidr="10.1.2.0/24")

        # Se crean las maquinas virtuales
        azure_driver.baseCompute.create_vm(name="bastion_vm_priv",
                                           subnet=azure_bastion_priv_subnet,
                                           public_key_file_path='/Volumes/Datos/Users/diegomendez29/.ssh/id_rsa.pub')

        aws_driver.networking.connect_networks(aws_bastion_vpc, azure_bastion_vpc)
