from PyVCR.rest_vcenter import rest_functions
ru=rest_functions()
ru.set_session()
vms=ru.get_all_vm()
print (vms)

#TODO API Explorer investigate this