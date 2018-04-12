# Test Sprint 3

import unittest

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver


class TestSprint3(unittest.TestCase):

    def test_sprint_3(self):

        auth_driver = VaultAuthDriver('token', 'bas7ion')
        provider_creds = auth_driver.get_providers_info()

        # Se obtiene driver de AWS
        aws_driver = Driver.create(provider_creds[0])

        # Se crea la red
        network = aws_driver.networking.create_network(name="Bas7ionNetwork",
                                                       cidr="10.0.0.0/16")

        # Se crea gateway para la red
        gateway = aws_driver.networking.create_gateway("Bas7ionGateway")

        # Asocia el gateway con la red
        network.attach_gateway(gateway)

        # Se crean las subredes
        subnet1 = network.create_subnet(name="Bas7ionSubnet1",
                                        cidr="10.0.0.0/24")
        subnet2 = network.create_subnet(name="Bas7ionSubnet2",
                                        cidr="10.0.1.0/24")

        # Busco Default RouteTable
        route_table = network.list_route_tables()[0]

        # Se agrega entrada en la tabla de ruteo para visibilidad entre subredes
        route_table.create_subnet_association(subnet1)
        route_table.create_subnet_association(subnet2)

        # Se agrega entrada por defecto al gateway
        route_table.create_route('0.0.0.0/0', gateway)

        # Busco default security group
        security_group = network.list_security_groups()[0]

        # Abro puertos del ssh y telnet
        security_group.allow_inbound_traffic(22)
        security_group.allow_inbound_traffic(23)

        # Se crean las interfaces de red
        nic1 = subnet1.create_nic(name="Bas7ionNetworkInterface1",
                                  private_ip="10.0.0.5")
        nic2 = subnet2.create_nic(name="Bas7ionNetworkInterface2",
                                  private_ip="10.0.1.5")

        # Se crean las maquinas virtuales
        vm1 = aws_driver.baseCompute.create_vm(name="Bas7ionVM1", subnet=subnet1, key_pair_name='aws_node')
        vm2 = aws_driver.baseCompute.create_vm(name="Bas7ionVM2", subnet=subnet2, key_pair_name='aws_node')

        # Se asocian las interfaces a las vms
        vm1.attach_nic(nic1)
        vm2.attach_nic(nic2)

        # Se provisiona la vm1 con la receta de mysql
        vm1.provision('/Users/laureanok/Documents/Bas7ion/ansible-receipts/wrappers/jenkins.yml', ['-vvvv'])

        # Se provisiona la vm2 con la receta de tomcat
        vm2.provision('/Users/laureanok/Documents/Bas7ion/ansible-receipts/wrappers/gitlab.yml', ['-vvvv'])

        # Conectar por ssh vm1

        # Instalar telnet vm1
        # sudo yum -y install telnet

        # Probar conexion contra vm2
        # telnet 10.0.1.5 22


