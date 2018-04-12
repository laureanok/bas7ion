import json
import time
import math

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver
from bastion.networking.base import Networking
from utils import VAULT_TOKEN_TEST

start_time = time.time()

# Se obtienen las credenciales
auth_driver = VaultAuthDriver(VAULT_TOKEN_TEST)
aws_cred = auth_driver.get_provider_info('secret/casoexito/aws')
azure_cred = auth_driver.get_provider_info('secret/casoexito/azure')

# Se obtiene driver de AWS
driver_aws = Driver.create(aws_cred)

# # Se obtiene driver de Azure
driver_azure = Driver.create(azure_cred)

# Se crea la red de AWS
network_aws = driver_aws.networking.create_network(name="Bas7ionVPC-CE-App",
                                                   cidr="200.0.0.0/16")

# Se crea la red de Azure
network_azure = driver_azure.networking.create_network(name="Bas7ionVPC-CE-DB",
                                                       cidr="200.1.0.0/16")

# Se crea las subred de AWS
subnet_aws = network_aws.create_subnet(name="Bas7ionSubnet-CE-App",
                                       cidr="200.0.1.0/24")

# Se crea las subred de la Azure
subnet_azure = network_azure.create_subnet(name="Bas7ionSubnet-CE-DB",
                                           cidr="200.1.1.0/24")

# Se crea la maquina virtual donde se intalara la Base de Datos MySQL
vm_db = driver_azure.baseCompute.create_vm(name="Bas7ionVM-DB",
                                           image_id='Canonical:UbuntuServer:14.04.5-LTS:latest',
                                           subnet=subnet_azure)

# Se crea la maquina virtual donde se instalara la Application Redmine
vm_app = driver_aws.baseCompute.create_vm(name="Bas7ionVM-App",
                                          image_id='ami-a042f4d8',
                                          subnet=subnet_aws)
# Se conectan las redes AWS y Azure
Networking.connect_networks(network_aws, network_azure)

# Se aprovisiona la maquina virtual de la Base de Datos instalando y configurando MySQL
mysql_playbook_path = 'playbooks/bennojoy-mysql.yml'
vm_db.provision(playbook_path=mysql_playbook_path)

# Se aprovisiona la maquina virtual de la aplicacion instalando y configurando Redmine
redmine_application_port = '8080'
redmine_parameters =\
    {
        'database_host': vm_db.private_ips[0],
        'application_port': redmine_application_port
    }

redmine_playbook_path = 'playbooks/bngsudheer-redmine.yml'
vm_app.provision(playbook_path=redmine_playbook_path,
                 parameters=json.dumps(redmine_parameters),
                 user='centos')

# Se habilita el puerto de la aplicacion para acceder desde internet
security_group = network_aws.list_security_groups()[0]
security_group.allow_inbound_traffic(redmine_application_port)

sec = time.time() - start_time
min = math.floor(sec / 60)
sec = math.floor(sec % 60)

print "Tiempo de ejecucion: %0.fm %0.fs" % (min, sec)

