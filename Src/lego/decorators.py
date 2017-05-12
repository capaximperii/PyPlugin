from functools import wraps

# Decorators
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
