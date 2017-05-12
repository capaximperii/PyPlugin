"""
Demonstrates use in every blueprint of the app module.

"""
from plugins import *
from lego import PluginBase
from marshmallow_jsonschema import JSONSchema

def main():
    """
    Demonstrates calling plugin methods.
    
    """
    plugins = PluginBase.get_plugins()
    json_schema = JSONSchema()

    for test in plugins:
        test.get_input_configuration()
        test.get_chart_configuration()
        test.get_modes_of_operation()
        print(test.dump(test).data)
        print(json_schema.dump(test).data)

if __name__ == '__main__':
    main()
