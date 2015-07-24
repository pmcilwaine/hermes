# /usr/bin/env python
# -*- coding: utf-8 -*-
from hermes_cms.core.registry_resolver import RegistryResolver


def import_handler(module_name, class_name):
    mod = __import__(module_name, fromlist=[str(class_name)])
    return getattr(mod, class_name)

class Service(object):
    """
    :type job_class: hermes_cms.service.job.Job
    """

    def __init__(self, name, region, config):
        """

        :type name: str
        :param name: Name of the job
        :type region: str
        :param region: The region code e.g. ap-southeast-2
        :type config: dict
        :param config: Complete job file dictionary
        """
        job_config = config['jobs'][name]
        self.service_config = job_config.get('service', {})
        self._resolve = RegistryResolver()
        self.region = region

        service_module = self.service_config.get('service_module')
        service_class = self.service_config.get('service_class')

        if not service_module or not not service_class:
            pass  # todo raise exception

        job_class = import_handler(service_module, service_class)
        self.job_class = job_class()

    def do_action(self):
        raise NotImplementedError('Method do_work is not implemented')
