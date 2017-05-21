"""
The base for all plugins to derive from. It also implements an auto registering pattern so that
the plugins do not have to explicitly register.

"""

import abc

from marshmallow_jsonschema import JSONSchema
from .decorators import check_chart_configuration
from .decorators import check_input_configuration
from .decorators import check_modes_of_operation
from .decorators import run_async
from .Datatypes import InputParams
# Plugin implementation

class PluginBase(metaclass=abc.ABCMeta):
    """
    The base class for all plugins that want to register with this application.

    """
    plugin_registry = {}
    def __init__(self, name, group):
        """
        Constructor to initialize basic fields.

        """
        self.name = name
        self.group = group
        self.input_params = InputParams()

    def __new__(cls, name, group, *args, **kwargs):
        """
        Factory method for base/subtype creation. Simply creates an
        (new-style class) object instance and sets a base property.
        """
        del args
        del kwargs
        instance = object.__new__(cls)
        # Call base class constructors by default to avoid doing them in each plugin.
        super(cls, instance).__init__(name, group)
        typedef = cls.__dict__
        for attr in typedef:
            func = typedef[attr]
            if hasattr(func, "__dont_decorate__"):
                pass
            elif callable(func) and func.__name__ == 'get_input_configuration':
                setattr(cls, attr, check_input_configuration(func))
            elif callable(func) and func.__name__ == 'get_chart_configuration':
                setattr(cls, attr, check_chart_configuration(func))
            elif callable(func) and func.__name__ == 'get_modes_of_operation':
                setattr(cls, attr, check_modes_of_operation(func))
            elif callable(func) and func.__name__ == 'run':
                setattr(cls, attr, run_async(func))

        if group not in cls.plugin_registry.keys():
            cls.plugin_registry[group] = []
        cls.plugin_registry[group].append(instance)
        return instance

    @classmethod
    def get_plugins(cls):
        """
        Gets the list of all plugins registered.

        """
        return cls.plugin_registry

    @classmethod
    def get_plugins_group(cls, group):
        """
        Gets plugins registered under a single group name.

        """
        if not group in cls.plugin_registry.keys():
            return None
        return cls.plugin_registry[group]

    def get_plugin_name(self):
        """
        returns the plugin name.

        """
        return self.name

    def get_plugin_group(self):
        """
        returns plugin family name.

        """
        return self.group

    def get_input_configuration(self):
        """
        Get name and type json value for input parameters required by this plugin to operate.

        """
        json_schema = JSONSchema()
        schema_blue_print = self.input_params.generate_schema(self.name + 'InputParams')
        schema_desc = schema_blue_print()
        return json_schema.dump(schema_desc).data

    @abc.abstractmethod
    def get_chart_configuration(self):
        """
        Get name and type json value for chart display for this plugin.

        """
        return None

    @abc.abstractmethod
    def get_modes_of_operation(self):
        """
        Get supported modes of operation online or offline

        """
        return ['online', 'offline']

    @abc.abstractmethod
    def run(self):
        """
        Run method to call for the plugin processing.

        """
        print("Running abstract method")
        return
