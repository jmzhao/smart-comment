import parse_library as plib
import parse_doc as pdoc
import parse_code as pcod
import itertools
import inspect, dis

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
    
interested_libs = plib.interested_libs

d = plib.gather(interested_libs)
ll = [plib.serialize_library_info(d[lib_name]) for lib_name, _ in interested_libs]

l_interested = list(filter(is_interested_obj, itertools.chain(*ll)))

l_code = list(map(get_code, l_interested))

l_doc = list(map(get_doc, l_interested))
l_doc = list(map(pdoc.extract, l_doc))