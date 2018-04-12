import unittest

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver


class TestAllOperations(unittest.TestCase):

    def test_all_operations(self):

        auth_driver = VaultAuthDriver('9c2547a0-d02d-20e5-82dd-c3be23e02573')
        provider_creds = auth_driver.get_providers_info('secret/project1')

        # Se obtiene driver de AWS
        aws_driver = Driver.create(provider_creds[0])

        # Se listan las imagenes
        aws_images = aws_driver.baseCompute.list_images()
        print "AWS Images: ", len(aws_images)

        # Se listan los tamanos
        aws_sizes = aws_driver.baseCompute.list_sizes()
        print "AWS Sizes: ", len(aws_sizes)

        # Se listan las VMs
        aws_vms = aws_driver.baseCompute.list_vms()
        print "AWS VMs: ", len(aws_vms)

        # Se obtiene driver de Azure
        azure_driver = Driver.create(provider_creds[1])

        # Se listan las imagenes
        azure_images = azure_driver.baseCompute.list_images()
        print "Azure Images: ", len(azure_images)

        # Se listan los tamanos
        azure_sizes = azure_driver.baseCompute.list_sizes()
        print "Azure Sizes: ", len(azure_sizes)

        # Se listan las VMs
        azure_vms = azure_driver.baseCompute.list_vms()
        print "Azure VMs: ", len(azure_vms)
