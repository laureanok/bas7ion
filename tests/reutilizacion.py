import time
import math

from bastion.authentication.vault import VaultAuthDriver
from bastion.driver import Driver
from utils import VAULT_TOKEN_TEST

start_time = time.time()

# Se el driver de autenticacion
auth_driver = VaultAuthDriver(VAULT_TOKEN_TEST)
# Se obtienen las credenciales de AWS
cred = auth_driver.get_provider_info('secret/reutilizacion/aws')
# Se obtienen las credenciales de Azure
#cred = auth_driver.get_provider_info('secret/reutilizacion/azure')

# Se obtiene driver
driver = Driver.create(cred)

# Se crea la red
network = driver.networking.create_network(name="Bas7ionVPC-R",
                                           cidr="100.0.0.0/16")

# Se crean las subredes
subnet = network.create_subnet(name="Bas7ionSubnet-R",
                                cidr="100.0.1.0/24")

# Se crean las maquinas virtuales
vm = driver.baseCompute.create_vm(name="Bas7ionVM-R",
                                   subnet=subnet)

sec = time.time() - start_time
min = math.floor(sec / 60)
sec = math.floor(sec % 60)

print "Tiempo de ejecucion: %0.fm %0.fs" % (min, sec)
