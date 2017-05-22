"""
Facilitates data exchange between different processes using mmap shared memory.

"""
import os
import mmap

import struct

class _ShmemMeta:
    """
    Implements index for mmap space.

    """
    def __init__(self):
        """
        Initializes index.

        """
        self.size_of_objects = 0
        self.number_of_objects = 0
        self.size_of = 0
        self.size_of = len(self.get_bytes())

    def set_size(self, size):
        """
        Sets size of objects, common for all objects.

        """
        self.size_of_objects = size

    def added_object(self):
        """
        Increments after each object is added.

        """
        self.number_of_objects += 1

    def get_size_of_object(self):
        """
        Returns size of individual object.

        """
        return self.size_of_objects

    def get_number_of_objects(self):
        """
        Returns number of objects.

        """
        return self.number_of_objects

    def get_bytes(self):
        """
        Converts this class into byte representation.

        """
        return struct.pack('@ii', self.size_of_objects, self.number_of_objects)

    def from_bytes(self, sbyte):
        """
        Loads this object from byte representation.

        """
        self.size_of_objects, self.number_of_objects = struct.unpack('@ii', sbyte)

    def size_of_meta(self):
        """
        Returns size of meta table.
        """
        return len(self.get_bytes())

    def __repr__(self):
        return str(self.number_of_objects) + ' each of size ' + str(self.size_of_objects)

class Shmem():
    """
    Inter process communication mechanism.

    """
    def __init__(self, taskid, child=True):
        """
        Initialize a shared memory block to share data between processes.

        """
        self.meta = None
        self.sharedmem = None
        self.size = 16384
        self._create_shmem(taskid, child)


    def _create_shmem(self, taskid, child):
        self.meta = _ShmemMeta()
        if child is False:
            if os.name == 'nt':
                self.sharedmem = mmap.mmap(-1, self.size, tagname='/tmp/fullsight.' + str(taskid))
            else:
                self.sharedmem = mmap.mmap(os.open('/tmp/fullsight.' + str(taskid)).fileno(),
                                           self.size, access=mmap.ACCESS_READ)
        else:
            if os.name == 'nt':
                self.sharedmem = mmap.mmap(-1, self.size, tagname='/tmp/fullsight.' + str(taskid))
            else:
                self.sharedmem = mmap.mmap(os.open('/tmp/fullsight.' + str(taskid)).fileno(),
                                           self.size, access=mmap.ACCESS_WRITE)
            self.sharedmem.write(self.meta.get_bytes())
        self.sharedmem.seek(0)
        self.meta.from_bytes(self.sharedmem.read(self.meta.size_of_meta()))

    def read_shmem(self):
        """
        Reads shared memory.

        """
        objs = []
        self.sharedmem.seek(0)
        self.meta.from_bytes(self.sharedmem.read(self.meta.size_of_meta()))
        for _ in range(self.meta.get_number_of_objects()):
            obj = self.sharedmem.read(self.meta.get_size_of_object())
            objs.append(obj)
        print(len(objs))
        return objs

    def append_shmem(self, obj):
        """
        Appends to shared memory.

        """
        current = self.sharedmem.tell()
        self.sharedmem.seek(0)
        self.meta.set_size(len(obj))
        self.meta.added_object()
        self.sharedmem.write(self.meta.get_bytes())
        self.sharedmem.seek(current)
        self.sharedmem.write(obj)

