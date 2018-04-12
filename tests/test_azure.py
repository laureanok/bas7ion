# Test Azure

from unittest import TestCase

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver


class TestAzure(TestCase):
    def create_network(self):
        auth_driver = VaultAuthDriver('token', 'bas7ion')
        provider_creds = auth_driver.get_providers_info()

        # Se obtiene driver de Azure
        azure_driver = Driver.create(provider_creds[1])

        # Se crea la red
        network = azure_driver.networking.create_network(name="Bas7ionNetwork",
                                                         cidr="10.0.0.0/16")

        # Se crea la subred
        subnet = network.create_subnet(name="Bas7ionSubnet",
                                       cidr="10.0.0.0/24")

    def create_azure_vm(self):
        auth_driver = VaultAuthDriver('token', 'bas7ion')
        provider_creds = auth_driver.get_providers_info ()

        # Se obtiene driver de Azure
        azure_driver = Driver.create (provider_creds[1])
        vm = azure_driver.baseCompute.create_vm()

    def test_create_local_network_gateway(self):
        auth_driver = VaultAuthDriver('token', 'bas7ion')
        provider_creds = auth_driver.get_providers_info()

        # Se obtiene driver de Azure
        azure_driver = Driver.create(provider_creds[1])

        libcloud = azure_driver.get_cloud_driver()

        locations = libcloud.list_locations()
        location = [l for l in locations if l.name == azure_driver.prop.location_id][0]

        r = libcloud.ex_create_local_network_gateway("TestLocalNetworkGateway", "192.168.0.0/16", "52.89.14.84", "LibcloudRG071407", location=location)

