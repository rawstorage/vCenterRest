from PyVCR.rest_vcenter import rest_functions
vc=rest_functions()
vc.set_session()
vms=vc.get_all_vm()
hosts=vc.get_hosts()
network=vc.get_network()
datastores=vc.get_datastores()
mydatastore=vc.get_datastore_config('datastore-20')

print (vms)
print (hosts)
print (network)
print(datastores)
print (mydatastore)
#TODO API Explorer investigate this