import os
import imp
from pathtools import path


def load_module(module):
    if not module.endswith('.py') or module.endswith('__init__.py'):
        return
    imp.load_source(name=os.path.basename(module), pathname=module)
    # return imp.load_module(__file__, *module["info"])

PLUGIN_PATH = os.path.dirname(__file__)
print("MAPPING", PLUGIN_PATH)
for module in path.list_files(PLUGIN_PATH, recursive=False):
    load_module(module)
# , action=(lambda module: load_module(module)))