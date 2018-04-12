from __future__ import absolute_import

import unittest

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver, AWSDriver, AzureDriver


class TestNodeDriver(unittest.TestCase):

    """
    def test_create_vm(self):
        auth_driver = AuthDriver('token', 'bas7ion')
        provider_creds = auth_driver.get_providers_info()

        drivers = []

        for cred in provider_creds:
            drivers.append(Driver.create(cred))

        for driver in drivers:
            if isinstance(driver, AWSDriver):
                print "AWS Driver exclusive ops"
            if isinstance(driver, AzureDriver):
                print "Azure Driver exclusive ops"
            driver.baseCompute.create_vm()

            # crea la virtual en AWS
            # aws_driver = Driver.create(provider_creds[0])
            # aws_driver.baseCompute.create_vm()

            # crea la virtual en Azure
            # azure_driver = Driver.create(provider_creds[1])
            # azure_driver.baseCompute.create_vm()

    def deploy_vm(self):
        auth_driver = AuthDriver('token', 'bas7ion')
        provider_creds = auth_driver.get_providers_info()

        drivers = []

        for cred in provider_creds:
            drivers.append(Driver.create(cred))

        for driver in drivers:
            if isinstance(driver, AWSDriver):
                print "AWS Driver exclusive ops"
            if isinstance(driver, AzureDriver):
                print "Azure Driver exclusive ops"

        if isinstance(drivers[0], AWSDriver):
            drivers[0].baseCompute.deploy_vm()

        # crea la virtual en AWS
        # aws_driver = Driver.create(provider_creds[0])
        # aws_driver.baseCompute.create_vm()

        # crea la virtual en Azure
        # azure_driver = Driver.create(provider_creds[1])
        # azure_driver.baseCompute.create_node()
    """

    def test_create_aws_network(self):

        auth_driver = VaultAuthDriver('e38fe1a8-68f4-f5f7-7039-862136f565f8')
        cred = auth_driver.get_provider_info('secret/project1/aws')

        # Se obtiene driver
        driver = Driver.create(cred)

        # Se crea la red
        network = driver.networking.create_network(name="Bas7ionNetwork",
                                                   cidr="10.0.0.0/16")

        # Se crean las subredes
        subnet1 = network.create_subnet(name="Bas7ionSubnet1",
                                        cidr="10.0.1.0/24")
        subnet2 = network.create_subnet(name="Bas7ionSubnet2",
                                        cidr="10.0.2.0/24")

if __name__ == '__main__':
    unittest.main()
