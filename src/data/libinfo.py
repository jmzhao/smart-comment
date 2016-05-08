# -*- coding: utf-8 -*-
"""
Library-specific information to help gather Python entities.
This is more or less like a configuration file.
"""

stop_module_names = ('test', 'tests', 'testing')

interested_libs = [
    ('sklearn', 
     lambda mn : (
        mn.split('.')[1] not in ('externals',) 
        and all(word not in mn.split('.') for word in stop_module_names))), 
    ('numpy', 
     lambda mn : (
        mn.split('.')[1] not in ('distutils', 'f2py') 
        and all(word not in mn.split('.') for word in stop_module_names))), 
    ('scipy', None),
]
