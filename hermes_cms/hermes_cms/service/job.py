# /usr/bin/env python
# -*- coding: utf-8 -*-


class InvalidJobError(Exception):
    pass


class FatalJobError(Exception):
    pass


class Job(object):

    def do_work(self, message=None):
        """
        The the work for this job.

        @param message A message to pass to the job.
        :return:
        """
        pass
