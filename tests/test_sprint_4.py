# Test Sprint 4

import unittest

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver


class TestSprint4(unittest.TestCase):

    def sprint_4(self):
        auth_driver = VaultAuthDriver('be30f966-9953-ee20-5cad-db98d7e58494')
        provider_creds = auth_driver.get_providers_info('secret/project1')

        # Se obtiene driver de Azure
        azure_driver = Driver.create(provider_creds[1])

        cloud_driver = azure_driver.get_cloud_driver()

        cloud_driver.ex_update_network(cidr_block="10.0.0.0/16",
                                       name="Bas7ionNetwork",
                                       resource_group=azure_driver.prop.resource_group,
                                       location_id=azure_driver.prop.location_id,
                                       dns_server="10.0.0.20")

    def test_sprint_4(self):

        auth_driver = VaultAuthDriver('48116d15-9d2f-669e-a0c4-eb8e6a0cbf2b')
        secrets = auth_driver.get_provider_info('secret/project1/')

        # Se obtiene driver de Azure
        cloud_provider_driver = Driver.create(secrets[1])

        # Se crea la red
        network = cloud_provider_driver.networking.create_network(name="Bas7ionNetwork",
                                                                  cidr="10.0.0.0/16")

        # Se crean las subredes
        subnet = network.create_subnet(name="Bas7ionSubnet1",
                                       cidr="10.0.0.16/28")
        # Se crea la VM
        vm = cloud_provider_driver.baseCompute.create_vm(name="Bas7ionVM1",
                                                         subnet=subnet,
                                                         public_key_file_path='/Users/laureanok/.ssh/id_rsa.pub')

        # Se provisiona la vm con una receta
        vm.provision(playbook_path='/Users/laureanok/Documents/Bas7ion/ansible-receipts/wrappers/mysql.yml',
                     additional_options=['-vvvv'])
