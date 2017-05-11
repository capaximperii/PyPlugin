"""
The base for all plugins to derive from. It also implements an auto registering pattern so that
the plugins do not have to explicitly register.

"""

import abc

from functools import wraps
from marshmallow_sqlalchemy import ModelSchema

# Decorators
def generate_schema(cls):
    """
    Automatically generate json schema for each plugin model.

    """
    class Schema(ModelSchema):
        """
        Automatically attach Schema to model.

        """
        class Meta:
            """
            Meta class for schema generation.

            """
            model = cls
    cls.Schema = Schema
    return cls

def check_input_configuration(func):
    """
    Checks input format registered by a plugin.

    """
    @wraps(func)
    def decorator(self, *args, **kwargs):
        """
        Implements wrapper.

        """
        try:
            print('enter input configuration')
            ret = func(self, *args, **kwargs)
            print('leave')
        except BaseException as exp:
            print('exception', exp)
            ret = None

        return ret
    return decorator

def check_chart_configuration(func):
    """
    Checks chart format registered by a plugin.

    """
    @wraps(func)
    def decorator(self, *args, **kwargs):
        """
        Implements wrapper.

        """
        try:
            print('enter chart configuration')
            ret = func(self, *args, **kwargs)
            print('leave')
        except BaseException as exp:
            print('exception', exp)
            ret = None

        return ret
    return decorator

def check_modes_of_operation(func):
    """
    Checks mode operation registered by a plugin.

    """
    @wraps(func)
    def decorator(self, *args, **kwargs):
        """
        Implements wrapper.

        """
        try:
            print('enter operation')
            ret = func(self, *args, **kwargs)
            print('leave')
        except BaseException as exp:
            print('exception', exp)
            ret = None

        return ret
    return decorator

def dont_decorate(func):
    """
    Decorator to be used to skip auto-decoration of functions.

    """
    func.__dont_decorate__ = True
    return func


# Plugin implementation

class PluginBase(metaclass=abc.ABCMeta):
    """
    The base class for all plugins that want to register with this application.

    """
    plugin_registry = []

    def __new__(cls, *args, **kwargs):
        """
        Factory method for base/subtype creation. Simply creates an
        (new-style class) object instance and sets a base property.
        """
        del args
        del kwargs
        instance = object.__new__(cls)
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



class Test(PluginBase):
    """
    Unit test class.

    """
    def __init__(self):
        """
        Constructor

        """
        print("Test constructor")

    def get_input_configuration(self):
        return "Yay"

    def get_chart_configuration(self):
        return "Noo"

    def get_modes_of_operation(self):
        return "yaas"

    def run(self):
        return None

if __name__ == '__main__':
    TEST = Test()
    TEST.get_input_configuration()
    TEST.get_chart_configuration()
    TEST.get_modes_of_operation()
