# /usr/bin/env python
# -*- coding: utf-8 -*-


def load_class(module_name, class_name, *args, **kwargs):
    mod = __import__(module_name, fromlist=[str(class_name)])
    the_class = getattr(mod, class_name)
    return the_class(*args, **kwargs)
