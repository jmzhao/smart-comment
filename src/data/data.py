# -*- coding: utf-8 -*-

from . import parselib as plib
from . import parsedoc as pdoc
from . import libinfo
import itertools

def is_interested_obj(obj) :
    try :
        doc = obj.__doc__
        code = obj.__code__
    except AttributeError :
        return False
    return doc is not None and code is not None

def get_code(obj) :
    return obj.__code__
    
def get_doc(obj) :
    return obj.__doc__

def get_entity_list(interested_libs) :
    d = plib.gather(interested_libs)
    ll = [plib.serialize_library_info(d[lib_name]) for lib_name, _ in interested_libs]
    
    l_interested = list(filter(is_interested_obj, itertools.chain(*ll)))
    return l_interested