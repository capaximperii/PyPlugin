"""
Defines datatypes to be declared and used by plugins.

"""
"""
Runtime structure to python mapping for sharing data between processes written in python
or other languages.

"""
import re
import struct
from collections import namedtuple

class RuntimeMonitorParams:
    """
    Class defines compatible type to share data with external application via shared memory or
    mmap pages.

    """
    C_TYPE_TO_PY_STRUCT = {
        'char':                 's',
        'signed char':          'b',
        'unsigned char':        'B',
        'short':                'h',
        'short int':            'h',
        'ushort':               'H',
        'unsigned short':       'H',
        'unsigned short int':   'H',
        'int':                  'i',
        'unsigned int':         'I',
        'long':                 'l',
        'long int':             'l',
        'unsigned long':        'L',
        'unsigned long int':    'L',
        'long long':            'q',
        'unsigned long long':   'Q',
        'float':                'f',
        'double':               'd',
        'void *':               'P',
        'int8':                 'b',
        'uint8':                'B',
        'int16':                'h',
        'uint16':               'H',
        'int32':                'i',
        'uint32':               'I',
        'int64':                'l',
        'uint64':               'L',
    }
    def __init__(self, byte_order='NATIVE'):
        """
        Constructor defines the endianness of the system where it is running.

        """
        defs = {'NATIVE' : '@', 'LITTLE-ENDIAN': '<', 'BIG-ENDIAN': '>'}
        self.type_def = defs[byte_order]
        self.var_names = []
        self.string_positions = []
        self.counter = 0
        self.deserializer = None

    def add_unsigned_integer_field(self, name):
        """
        Adds an unsigned integer field

        """
        self.type_def += 'I'
        self.var_names.append(name)
        self.counter += 1

    def add_signed_integer_field(self, name):
        """
        Adds a signed integer field

        """
        self.type_def += 'i'
        self.var_names.append(name)
        self.counter += 1

    def add_signed_short_field(self, name):
        """
        Adds a signed short field

        """
        self.type_def += 'h'
        self.var_names.append(name)
        self.counter += 1

    def add_unsigned_short_field(self, name):
        """
        Adds an unsigned short field

        """
        self.type_def += 'H'
        self.var_names.append(name)
        self.counter += 1

    def add_signed_long_field(self, name):
        """
        Adds a signed long field

        """
        self.type_def += 'l'
        self.var_names.append(name)
        self.counter += 1

    def add_unsigned_long_field(self, name):
        """
        Adds an unsigned long field

        """
        self.type_def += 'L'
        self.var_names.append(name)
        self.counter += 1

    def add_float_field(self, name):
        """
        Adds an float field

        """
        self.type_def += 'f'
        self.var_names.append(name)
        self.counter += 1

    def add_double_field(self, name):
        """
        Adds an double field

        """
        self.type_def += 'd'
        self.var_names.append(name)
        self.counter += 1

    def add_string_field(self, name, max_size):
        """
        Adds an C style string field

        """
        self.type_def += str(max_size) + 's'
        self. var_names.append(name)
        self.string_positions.append(self.counter)
        self.counter += 1

    def serialize(self, obj):
        """
        Flatten the object to be saved into shared memory.

        """
        obj_as_list = list(obj)
        for spos in self.string_positions:
            obj_as_list[spos] = obj_as_list[spos].encode()
        return struct.pack(self.type_def, *obj_as_list)

    def deserialize(self, obj):
        """
        Create a python object out of memory bytes.

        """
        if self.deserializer is None:
            self.deserializer = namedtuple('RuntimeMonitorParamsDeserialized',
                                           field_names=self.var_names)

        obj = self.deserializer._make(struct.unpack(self.type_def, obj))
        obj_as_dict = obj._asdict()
        for spos in self.string_positions:
            string_value = getattr(obj, self.var_names[spos]).decode('utf-8')
            obj_as_dict[self.var_names[spos]] = string_value
        return self.deserializer(*obj_as_dict.values())
