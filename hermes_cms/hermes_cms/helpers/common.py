# /usr/bin/env python
# -*- coding: utf-8 -*-


def load_class(module_name, class_name, *args, **kwargs):
    the_class = load_module_class(module_name, class_name)
    return the_class(*args, **kwargs)


def load_module_class(module_name, class_name):
    mod = __import__(module_name, fromlist=[str(class_name)])
    return getattr(mod, class_name)