"""
The base for all plugins to derive from. It also implements an auto registering pattern so that
the plugins do not have to explicitly register.

"""

import abc

from marshmallow import Schema, post_dump
from .decorators import check_chart_configuration
from .decorators import check_input_configuration
from .decorators import check_modes_of_operation

# Plugin implementation

class PluginBase(Schema):
    """
    The base class for all plugins that want to register with this application.

    """
    plugin_registry = []
    def __init__(self):
        Schema.__init__(self)

    def __new__(cls, *args, **kwargs):
        """
        Factory method for base/subtype creation. Simply creates an
        (new-style class) object instance and sets a base property.
        """
        del args
        del kwargs
        instance = object.__new__(cls)
        # Call base class constructors by default to avoid doing them in each plugin.
        super(cls, instance).__init__()
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
        cls.plugin_registry.append(instance)
        return instance

    @classmethod
    def get_plugins(cls):
        """
        Gets the list of all plugins registered.

        """
        return cls.plugin_registry

    @abc.abstractmethod
    def get_input_configuration(self):
        """
        Get name and type json value for input parameters required by this plugin to operate.

        """
        return None

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

    @post_dump
    def add_extra_field(self, output):
        """
        Add extra field for sake of poc.

        """
        output['plugin_name'] = type(self).__name__
        return output
