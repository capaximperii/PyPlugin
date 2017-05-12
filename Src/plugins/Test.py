"""
Example of a plugin implementaion.

"""
from lego import PluginBase
from marshmallow import fields

class Test(PluginBase):
    """
    Unit test class.

    """
    ident = fields.Int()
    name = fields.String()

    def __init__(self):
        """
        Constructor

        """
        # pylint: disable=W0231
        print("Test constructor")

    def get_input_configuration(self):
        """
        Define some input configuration to display input form.

        """
        return "Yay"

    def get_chart_configuration(self):
        """
        Defines chart configuration to display.

        """
        return "Noo"

    def get_modes_of_operation(self):
        """
        Get modes that this plugin operates in.

        """
        return "yaas"

    def run(self):
        """
        Runs the tool.

        """
        return None


CREATE_ONE_OBJECT = Test() # The framework does the rest.
