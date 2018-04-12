import unittest
import re
from netaddr import IPNetwork

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver
from bastion.test.utils import VAULT_TOKEN_TEST

class TestCompute(unittest.TestCase):

    def test_compute(self):
        auth_driver = VaultAuthDriver(VAULT_TOKEN_TEST)
        cred = auth_driver.get_provider_info('secret/credCompute')

        # Se obtiene driver
        driver = Driver.create(cred)

        # Se listan las imagenes
        images = driver.baseCompute.list_images()
        print "Images:"
        for image in images:
            text = "Id: " + image.id
            if image.name is not None:
                text = text + " Name: " + image.name
            print text

        # Se listan los tamanos
        sizes = driver.baseCompute.list_sizes()
        print "Sizes:"
        for size in sizes:
            text = "Id: " + size.id
            if size.name is not None:
                text = text + " Name: " + size.name
            print text
        # Create Virtual Machine
        vms1 = driver.baseCompute.create_vm(name="Bas7ionVM1-Compute")

        # Agrego una nueva interfaz a la VM
        subnet_ips = IPNetwork(vms1.subnet.cidr)
        new_private_ip = None
        index = 2
        while new_private_ip is None:
            if subnet_ips[index] != vms1.private_ips[0]:
                new_private_ip = subnet_ips[index]
            index = index + 1

        vms1.attach_nic(vms1.subnet.create_nic(new_private_ip, "Bas7ionVM1-Compute-nic2"))

        # Create Virtual Machine
        vms2 = driver.baseCompute.create_vm(name="Bas7ionVM2-Compute",
                                            add_public_ip=False)

        # Se listan las VMs
        vms = driver.baseCompute.baseCompute.list_vms()
        print "VMs:"
        for vm in vms:
            text = "Id: " + vm.id + " Name: " + vm.name
            print text

        # Se apaga la maquina virtual
        vms1.stop()

        # Se inicia la maquina virtual
        vms1.start()

        # Se reinicia la maquina virtual
        vms2.restart()

        # Se aproviciona la maquina virtual
        vms1.provision(playbook_path="playbooks/bennojoy-mysql.yml", user="ubuntu")

        # Se elimina la maquina virtual
        vms1.delete()
        vms2.delete()

