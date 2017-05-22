"""
InputParams used for dynamic form input generation.

"""

from marshmallow import Schema, fields, validate

class InputParams():
    """
    Defines the datatype schema generation on the fly.

    """
    def __init__(self):
        self.data_definition = {}

    def add_integer_field(self, name, validation, required=False):
        """
        Adds an integer field to the schema.

        """
        self.data_definition[name] = fields.Integer(validate=validation, required=required)

    def get_integer_range_validation(self, min_value, max_value):
        """
        Returns a validator for the integer field.

        """
        return validate.Range(min=min_value, max=max_value)

    def add_string_field(self, name, validation, required=False):
        """
        Adds a string field to the schema.

        """
        self.data_definition[name] = fields.String(validate=validation, required=required)

    def get_string_length_validation(self, min_length, max_length):
        """
        Returns a validator for the string length.

        """
        return validate.Length(min=min_length, max=max_length)

    def get_string_one_of_validate(self, choices):
        """
        Returns a validator for string selection from a set.

        """
        return validate.OneOf(choices=choices)

    def generate_schema(self, schema_name):
        """
        Generates the schema as a class from the data definition.

        """
        dyn_schema = type(schema_name, (Schema,), self.data_definition)
        return dyn_schema
