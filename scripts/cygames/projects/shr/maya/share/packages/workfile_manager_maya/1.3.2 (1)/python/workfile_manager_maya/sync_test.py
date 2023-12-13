from workfile_manager import p4utils
p4u = p4utils.P4Utils.get_instance()

res = p4u.p4_run_xxx('help')
print('res:', res)