"""
Demonstrates use in every blueprint of the app module.

"""
from plugins import *
from Lego import PluginBase
from Lego.Datatypes import RuntimeMonitorParams
from Lego.Ipc import Shmem

def main():
    """
    Demonstrates calling plugin methods.

    """
    groups = PluginBase.get_plugins()
    for k in groups.keys():
        plugins = groups[k]
        for test in plugins:
            print(test.get_input_configuration())
            test.get_chart_configuration()
            test.get_modes_of_operation()

    monitor = RuntimeMonitorParams()
    writer_ipc = Shmem(10, child=True)
    reader_ipc = Shmem(10, child=False)

    monitor.add_string_field('name', 20)
    monitor.add_unsigned_integer_field('score')
    monitor.add_signed_integer_field('credit')
    monitor.add_string_field('city', 20)

    obj = monitor.serialize(('Kush', 22, -1, 'hyd'))
    writer_ipc.append_shmem(obj)
    writer_ipc.append_shmem(obj)
    writer_ipc.append_shmem(obj)
    writer_ipc.append_shmem(obj)
    writer_ipc.append_shmem(obj)

    objs = reader_ipc.read_shmem()
    for obj in objs:
        after = monitor.deserialize(obj[:48])
        print(after.name)
        print(after.score)
        print(after.credit)
        print(after.city)

if __name__ == '__main__':
    main()
