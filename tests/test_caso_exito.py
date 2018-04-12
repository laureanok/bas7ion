import unittest
import json

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver
from bastion.networking.base import Networking
from bastion.test.utils import VAULT_TOKEN_TEST


class CasoExitoTest(unittest.TestCase):

    def test_caso_exito(self):
        # Se obtienen las credenciales
        auth_driver = VaultAuthDriver(VAULT_TOKEN_TEST)
        aws_cred_1 = auth_driver.get_provider_info('secret/project1/aws-us-west-2')
        aws_cred_2 = auth_driver.get_provider_info('secret/project1/azure-us-west')

        # Se obtiene driver
        driver1 = Driver.create(aws_cred_1)

        # # Se obtiene driver
        driver2 = Driver.create(aws_cred_2)

        # Se crea la red 1
        network1 = driver1.networking.create_network(name="Bas7ionVPC-1",
                                                     cidr="10.0.0.0/16")

        # Se crea la red 1
        network2 = driver2.networking.create_network(name="Bas7ionVPC-2",
                                                     cidr="10.1.0.0/16")

        # Se crea las subred de la red 1
        subnet1 = network1.create_subnet(name="Bas7ionSubnet-1",
                                         cidr="10.0.1.0/24")

        # Se crea las subred de la red 1
        subnet2 = network2.create_subnet(name="Bas7ionSubnet-2",
                                         cidr="10.1.1.0/24")

        # Se crea la maquina virtual
        vm_db = driver2.baseCompute.create_vm(name="Bas7ionVM-DB",
                                              image_id='Canonical:UbuntuServer:14.04.5-LTS:latest',
                                              subnet=subnet2)

        # Se crea la maquina virtual
        vm_app = driver1.baseCompute.create_vm(name="Bas7ionVM-App",
                                               image_id='ami-a042f4d8',
                                               subnet=subnet1)

        Networking.connect_networks(network1, network2)

        mysql_playbook_path = 'playbooks/bennojoy-mysql.yml'
        redmine_playbook_path = 'playbooks/bngsudheer-redmine.yml'

        redmine_application_port = '8080'

        vm_db.provision(playbook_path=mysql_playbook_path)

        redmine_parameters =\
            {
                'database_host': vm_db.private_ips[0],
                'application_port': redmine_application_port
            }

        vm_app.provision(playbook_path=redmine_playbook_path,
                         parameters=json.dumps(redmine_parameters),
                         user='centos')

        security_group = network1.list_security_groups()[0]
        security_group.allow_inbound_traffic(redmine_application_port)
