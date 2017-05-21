"""
Demonstrates use in every blueprint of the app module.

"""
from plugins import *
from Lego import PluginBase
from Lego.Datatypes import InputParams
from Lego.Datatypes import RuntimeMonitorParams
from marshmallow_jsonschema import JSONSchema
from Lego.Ipc import Ipc

def main():
    """
    Demonstrates calling plugin methods.

    """
    groups = PluginBase.get_plugins()
    json_schema = JSONSchema()

    for k in groups.keys():
        plugins = groups[k]
        for test in plugins:
            test.get_input_configuration()
            test.get_chart_configuration()
            test.get_modes_of_operation()
            # print(test.dump(test).data)
            # print(json_schema.dump(test).data)

    ddf = InputParams()
    validation = ddf.get_integer_range_validation(min_value=1, max_value=11)
    ddf.add_integer_field(name='luv', validation=validation)
    ddf.add_string_field(name="kush", validation=None, required=True)
    ddf = ddf.generate_schema('Josh')
    created = ddf()
    jscon = JSONSchema()
    print(jscon.dump(created).data)

    # plugins = groups['EventLogs']
    # for test in plugins:
    #     test.run(id=10)

    # print("Main thread")

    monitor = RuntimeMonitorParams()
    writer_ipc = Ipc(10, child=True)
    reader_ipc = Ipc(10, child=False)

    monitor.add_string_field('name', 20)
    monitor.add_unsigned_integer_field('age')
    monitor.add_signed_integer_field('credit')
    monitor.add_string_field('school', 20)

    obj = monitor.serialize(('Luv', 22, -1, 'ionis'))
    writer_ipc.append_shmem(obj)
    writer_ipc.append_shmem(obj)
    writer_ipc.append_shmem(obj)
    writer_ipc.append_shmem(obj)
    writer_ipc.append_shmem(obj)

    objs = reader_ipc.read_shmem()
    for obj in objs:
        after = monitor.deserialize(obj[:48])
        print(after.name)
        print(after.age)
        print(after.credit)
        print(after.school)

if __name__ == '__main__':
    main()
