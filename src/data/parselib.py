# -*- coding: utf-8 -*-
"""
Created on Mon May  2 21:54:11 2016

@author: jmzhao
"""

import logging
import inspect
import pkgutil
import importlib

logging.basicConfig(level=logging.INFO)

def get_info(entity, module) :
    """
    generate @code_info_dict for an given Python entity with the module
    """
    subs_list = list()
    for subname, sub in inspect.getmembers(entity, 
                                           lambda ns : inspect.isclass(ns) or inspect.isfunction(ns)) :
        if sub.__module__ != module.__name__ : continue
        try :
            logging.debug('get_info: working on %s %s'%(sub.__module__, sub.__name__))
            sub_dict = get_info(sub, module)
            subs_list.append(sub_dict)
        except TypeError :
            pass
    return {
        'entity' : entity,
        'sub' : subs_list,
    }
    
def get_library_info(libname, module_filter=None) :
    if module_filter is None :
        module_filter = lambda x : True
    
    package = importlib.import_module(libname)
    l = list()
    for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                      prefix=package.__name__+'.'
                                                      #onerror=lambda x: None
                                                      ):
        if not module_filter(modname) : continue
        logging.info('get_library_info: come with module %s'%(modname)) 
#        sub = importlib.import_module(modname)
        try :                                              
            sub = importlib.import_module(modname)
        except Exception as e :
            logging.warn(str(e))
#            warnings.warn(e.msg, ImportWarning)
            continue
        d = get_info(sub, sub)
        d['ispkg'] = ispkg
        l.append(d)
    return {'lib' : package, 'sub' : l}
    
def gather(interested_libs) :
    info = dict()
    for lib_name, module_filter in interested_libs :
        info[lib_name] = get_library_info(lib_name, module_filter)
    return info
    
def serialize_info(info) :
    l = [info['entity']]
    for sub_info in info['sub'] :
        l.extend(serialize_info(sub_info))
    return l
    
def serialize_library_info(lib_info) :
    l = []
    for entity_info in lib_info['sub'] :
        l.extend(serialize_info(entity_info))
    return l
    
if __name__ == '__main__' :
    from . import libinfo
    d = gather(libinfo.interested_libs)
    l = [serialize_library_info(d[lib_name]) for lib_name, _ in libinfo.interested_libs]