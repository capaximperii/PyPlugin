"""
Example of a plugin implementaion.

"""
from marshmallow import fields, validate
from Lego.PluginBase import PluginBase

class Analyze(PluginBase):
    """
    Analyze plugin implementation class.

    """
    ident = fields.Int(validate=validate.Range(min=1, max=10))
    name = fields.String(validate=validate.Length(min=3, max=40))

    def __init__(self, name, group):
        """
        Constructor

        """
        # pylint: disable=W0231
        print("Test constructor")

    # def get_input_configuration(self):
    #     """
    #     Define some input configuration to display input form.

    #     """
    #     return "Yay"

    def get_chart_configuration(self):
        """
        Defines chart configuration to display.

        """
        return "Noo"

    def get_modes_of_operation(self):
        """
        Get modes that this plugin operates in.

        """
        return ["Online", "Offline"]

    def run(self):
        """
        Runs the tool.

        """
        print("LASUN!!!!!!!!!!!!!!!!!!!!!!!!!")
        return None


CREATE_ONE_OBJECT = Analyze(name="Analyze", group="EventLogs") # The framework does the rest.
